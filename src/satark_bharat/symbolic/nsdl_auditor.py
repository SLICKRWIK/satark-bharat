"""NSDL & CDSL Depository Invariant Auditor (Specialized for NSDL Jury Alignment)."""

import re
from dataclasses import dataclass


@dataclass
class DepositoryAuditResult:
    detected_demat_ids: list[str]
    depository_type: str | None  # "NSDL", "CDSL", "INVALID_FORMAT", "NONE"
    is_valid_format: bool
    is_fake_nsdl_claim: bool
    statutory_violation: str | None
    penalty_points: int


class NsdlDepositoryAuditor:
    # NSDL Demat Account: 8-char DP ID (starts with IN + 6 digits) + 8-digit Client ID = 16 chars (IN\d{14})
    NSDL_DEMAT_REGEX = re.compile(r"\bIN\d{14}\b", re.IGNORECASE)
    # CDSL Demat Account is 16 purely numeric digits
    CDSL_DEMAT_REGEX = re.compile(r"\b\d{16}\b")
    # Fake NSDL claims (e.g. claiming "NSDL Approved Margin", "NSDL Institutional Allotment Pool", "NSDL Account Freeze")
    NSDL_COERCION_REGEX = re.compile(
        r"(nsdl\s+pool|nsdl\s+institutional|nsdl\s+guaranteed|nsdl\s+freeze\s+notice|nsdl\s+verification\s+fee)",
        re.IGNORECASE,
    )

    def audit_depository_claims(self, text: str) -> DepositoryAuditResult:
        nsdl_matches = self.NSDL_DEMAT_REGEX.findall(text)
        has_nsdl_coercion = bool(self.NSDL_COERCION_REGEX.search(text))

        detected_demat = [m.upper() for m in nsdl_matches]
        depository_type = "NSDL" if detected_demat else "NONE"
        is_valid = bool(detected_demat)

        penalty = 0
        violation = None

        # Check if fraudster claims NSDL approval for illegal pooling or fees
        if has_nsdl_coercion:
            penalty += 35
            violation = (
                "Unauthorized Misuse of NSDL Depository Name/Seal for Fraudulent Fund Solicitation "
                "(Depository Act, 1996 & SEBI Intermediary Fraud Regulations)"
            )

        return DepositoryAuditResult(
            detected_demat_ids=detected_demat,
            depository_type=depository_type,
            is_valid_format=is_valid,
            is_fake_nsdl_claim=has_nsdl_coercion,
            statutory_violation=violation,
            penalty_points=min(40, penalty),
        )
