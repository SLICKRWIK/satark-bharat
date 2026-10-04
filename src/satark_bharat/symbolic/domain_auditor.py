"""Deceptive Domain & Typosquatting Auditor using Permutation Analysis."""

import json
import re
from dataclasses import dataclass
from urllib.parse import urlparse

from satark_bharat.config import APK_REGEX, URL_REGEX, VERIFIED_DOMAINS_PATH


@dataclass
class DomainAuditResult:
    detected_urls: list[str]
    has_apk_link: bool
    is_typosquatted: bool
    spoofed_target: str | None
    suspicious_domain: str | None
    domain_entropy: float
    has_suspicious_tld: bool
    statutory_violation: str | None
    penalty_points: int


def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def calculate_shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    import math
    from collections import Counter
    counts = Counter(s)
    total = len(s)
    return round(-sum((count / total) * math.log2(count / total) for count in counts.values()), 2)


SUSPICIOUS_TLDS = {".trade", ".vip", ".top", ".click", ".icu", ".site", ".club", ".xyz", ".cc", ".buzz", ".work", ".link"}


class DomainAuditor:
    def __init__(self, verified_path=VERIFIED_DOMAINS_PATH):
        self.verified_targets = self._load_benchmarks(verified_path)

    def _load_benchmarks(self, path) -> list[str]:
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("exchanges_and_regulators", []) + data.get("top_registered_brokers", [])
            except Exception:
                pass
        return [
            "nseindia.com", "bseindia.com", "sebi.gov.in", "zerodha.com",
            "groww.in", "angelone.in", "upstox.com", "icicidirect.com"
        ]

    def extract_urls(self, text: str) -> list[str]:
        return list(dict.fromkeys(URL_REGEX.findall(text)))

    def check_apk(self, text: str) -> bool:
        return bool(APK_REGEX.search(text))

    def audit_domains(self, text: str) -> DomainAuditResult:
        urls = self.extract_urls(text)
        has_apk = self.check_apk(text)

        if not urls and not has_apk:
            return DomainAuditResult(
                detected_urls=[],
                has_apk_link=False,
                is_typosquatted=False,
                spoofed_target=None,
                suspicious_domain=None,
                domain_entropy=0.0,
                has_suspicious_tld=False,
                statutory_violation=None,
                penalty_points=0,
            )

        is_typosquatted = False
        spoofed_target = None
        suspicious_domain = None
        max_entropy = 0.0
        has_suspicious_tld = False

        for u in urls:
            parsed = urlparse(u)
            netloc = parsed.netloc.lower()
            if not netloc:
                netloc = parsed.path.lower().split("/")[0]

            # Strip port or www
            netloc = netloc.removeprefix("www.")

            # Calculate entropy
            entropy = calculate_shannon_entropy(netloc)
            if entropy > max_entropy:
                max_entropy = entropy

            # Check suspicious TLD
            if any(netloc.endswith(tld) for tld in SUSPICIOUS_TLDS):
                has_suspicious_tld = True

            # If perfectly matched with verified whitelist, safe
            if netloc in self.verified_targets:
                continue

            netloc_base = netloc.split(".")[0]
            # Normalize netloc base by removing common phishing suffixes/hyphens
            cleaned_base = re.sub(r"[-_](app|login|web|portal|trade|india|vip|official|bonus|auth|pro)", "", netloc_base)
            # Normalize common leetspeak substitutions
            normalized_base = cleaned_base.replace("0", "o").replace("1", "l").replace("3", "e").replace("4", "a")

            # Compare with each benchmark domain
            for target in self.verified_targets:
                target_base = target.split(".")[0]

                # Check exact substring containment or Levenshtein proximity
                dist = levenshtein_distance(cleaned_base, target_base)
                norm_dist = levenshtein_distance(normalized_base, target_base)

                if (
                    (dist <= 3 and len(cleaned_base) >= 4)
                    or (norm_dist <= 2 and len(normalized_base) >= 4)
                    or (target_base in netloc and netloc != target)
                ):
                    is_typosquatted = True
                    spoofed_target = target
                    suspicious_domain = netloc
                    break

            if is_typosquatted:
                break

        penalty = 0
        violations = []

        if has_apk:
            penalty += 40
            violations.append("Distribution of Unofficial Third-Party APK Terminal (High Malware Risk under IT Act 66D)")

        if is_typosquatted:
            penalty += 30
            violations.append(f"Deceptive Lookalike Domain '{suspicious_domain}' Spoofing Verified Entity '{spoofed_target}'")

        if has_suspicious_tld and not is_typosquatted:
            penalty += 15
            violations.append("High-Risk Deceptive Top-Level Domain (TLD) Associated with Financial Cyber Syndicates")

        statutory = " & ".join(violations) if violations else None

        return DomainAuditResult(
            detected_urls=urls,
            has_apk_link=has_apk,
            is_typosquatted=is_typosquatted,
            spoofed_target=spoofed_target,
            suspicious_domain=suspicious_domain,
            domain_entropy=max_entropy,
            has_suspicious_tld=has_suspicious_tld,
            statutory_violation=statutory,
            penalty_points=min(40, penalty),
        )
