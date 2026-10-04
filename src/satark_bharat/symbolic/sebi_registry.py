"""Deterministic SEBI Registration Invariant Validator & Offline Registry Cross-Reference."""

import json
import re
from dataclasses import dataclass
from typing import Any

from satark_bharat.config import (
    APK_REGEX,
    SEBI_GENERAL_REGEX,
    SEBI_PATTERNS,
    SEBI_REGISTRY_PATH,
    UPI_VPA_REGEX,
    URL_REGEX,
)


@dataclass
class SebiAuditResult:
    claimed_id: str | None
    is_valid_format: bool
    category: str | None
    is_in_registry: bool
    registered_entity_name: str | None
    registry_status: str  # "VERIFIED_ACTIVE", "NOT_FOUND", "INVALID_FORMAT", "NONE_CLAIMED", "NOT_APPLICABLE"
    is_impersonation_suspected: bool
    statutory_violation: str | None
    penalty_points: int


class SebiRegistryAuditor:
    FINANCIAL_ACTIVITY_REGEX = re.compile(
        r"(\b(nifty|banknifty|sensex|finnifty|stocks?|shares?|equit(y|ies)|options?|futures?|f&o|calls?|puts?|ce|pe|crypto|forex|demat|trading|intraday|delivery|dividend|portfolio|mutual\s+funds?|sip|ipo|circuit|guarantee(d)?|jackpot|paisa\s+double|sure[-\s]?shot|pakka\s+profit|fixed\s+returns?|vip\s+group|insider\s+pool|operator\s+setting|fees?|charges?|margin|deposit|transfer|paytm|gpay|phonepe)\b|₹|rs\.?|\b\d+%\s*(return|profit|gain))",
        re.IGNORECASE,
    )

    def __init__(self, registry_path=SEBI_REGISTRY_PATH):
        self.registry = self._load_registry(registry_path)

    def _load_registry(self, path) -> dict[str, Any]:
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def extract_sebi_ids(self, text: str) -> list[str]:
        """Extract candidate SEBI tokens using regex AST."""
        matches = SEBI_GENERAL_REGEX.findall(text)
        # Deduplicate while preserving case-normalized identifiers
        return list(dict.fromkeys([m.upper() for m in matches]))

    def determine_category(self, sebi_id: str) -> str | None:
        for category, pattern in SEBI_PATTERNS.items():
            if pattern.match(sebi_id):
                return category
        return None

    def audit_registration(
        self,
        text: str,
        claimed_name: str | None = None,
        is_financial_context: bool | None = None,
    ) -> SebiAuditResult:
        extracted_ids = self.extract_sebi_ids(text)

        if is_financial_context is None:
            has_financial_activity = (
                bool(self.FINANCIAL_ACTIVITY_REGEX.search(text))
                or bool(UPI_VPA_REGEX.search(text))
                or bool(URL_REGEX.search(text))
                or bool(APK_REGEX.search(text))
            )
        else:
            has_financial_activity = is_financial_context

        if not extracted_ids:
            # If input has no securities or transactional activity, absence of SEBI ID is completely lawful
            if not has_financial_activity:
                return SebiAuditResult(
                    claimed_id=None,
                    is_valid_format=False,
                    category=None,
                    is_in_registry=False,
                    registered_entity_name=None,
                    registry_status="NOT_APPLICABLE",
                    is_impersonation_suspected=False,
                    statutory_violation=None,
                    penalty_points=0,
                )

            # Absence of SEBI ID in an active investment advisory/return solicitation pitch is an offense under Sec 12(1)
            return SebiAuditResult(
                claimed_id=None,
                is_valid_format=False,
                category=None,
                is_in_registry=False,
                registered_entity_name=None,
                registry_status="NONE_CLAIMED",
                is_impersonation_suspected=False,
                statutory_violation="Section 12(1) SEBI Act 1992 (Unregistered Advisory Solicitation)",
                penalty_points=30,
            )

        primary_id = extracted_ids[0]
        category = self.determine_category(primary_id)
        is_valid_format = category is not None

        if not is_valid_format:
            return SebiAuditResult(
                claimed_id=primary_id,
                is_valid_format=False,
                category=None,
                is_in_registry=False,
                registered_entity_name=None,
                registry_status="INVALID_FORMAT",
                is_impersonation_suspected=False,
                statutory_violation="Invalid Alphanumeric SEBI Code Pattern",
                penalty_points=35,
            )

        # Check against offline verified snapshot
        entity_info = self.registry.get(primary_id)
        if entity_info:
            registered_name = entity_info.get("entity_name")
            # If a name was claimed, check for mismatch
            is_impersonation = False
            if claimed_name and registered_name:
                # Basic token overlap check
                c_tokens = set(claimed_name.lower().split())
                r_tokens = set(registered_name.lower().split())
                if not (c_tokens & r_tokens):
                    is_impersonation = True

            return SebiAuditResult(
                claimed_id=primary_id,
                is_valid_format=True,
                category=category,
                is_in_registry=True,
                registered_entity_name=registered_name,
                registry_status="VERIFIED_ACTIVE",
                is_impersonation_suspected=is_impersonation,
                statutory_violation="Potential Identity Spoofing of Licensed Entity" if is_impersonation else None,
                penalty_points=40 if is_impersonation else 0,
            )

        # Valid regex format, but not in official register
        return SebiAuditResult(
            claimed_id=primary_id,
            is_valid_format=True,
            category=category,
            is_in_registry=False,
            registered_entity_name=None,
            registry_status="NOT_FOUND",
            is_impersonation_suspected=True,
            statutory_violation="Fictitious Registration Number (Section 66D IT Act / SEBI Fraudulent Trade Practices)",
            penalty_points=35,
        )
