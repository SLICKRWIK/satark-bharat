"""Deterministic Threat Index Formula and Multi-Factor Penalty Engine."""

import re
from dataclasses import dataclass

from satark_bharat.symbolic.domain_auditor import DomainAuditor, DomainAuditResult
from satark_bharat.symbolic.payment_auditor import PaymentAuditResult, PaymentChannelAuditor
from satark_bharat.symbolic.sebi_registry import SebiAuditResult, SebiRegistryAuditor


@dataclass
class ThreatReport:
    composite_threat_score: int  # 0 to 100
    severity: str  # "LOW_RISK", "MODERATE_CAUTION", "HIGH_THREAT", "CRITICAL_FRAUD"
    guaranteed_returns_detected: bool
    urgency_fomo_detected: bool
    unregistered_pool_detected: bool
    red_line_triggered: bool
    red_line_reason: str | None
    sebi_audit: SebiAuditResult
    payment_audit: PaymentAuditResult
    domain_audit: DomainAuditResult
    statutory_violations: list[str]
    penalty_breakdown: dict[str, int]
    recommended_routing: str
    plain_english_summary: str
    vernacular_hindi_summary: str
    vernacular_bengali_summary: str


class ThreatIndexEngine:
    # Heuristic regex patterns for psychological coercion & illegal return promises
    GUARANTEED_PATTERNS = re.compile(
        r"(guaranteed\s+return|fixed\s+return|100%\s+jackpot|200%|500%|loss[-\s]?free|pakka\s+profit|sure[-\s]?shot|sureprofit|paisa\s+double|double\s+return)",
        re.IGNORECASE,
    )
    URGENCY_PATTERNS = re.compile(
        r"(hurry|only\s+\d+\s+slots?|immediate|expiry\s+special|valid\s+for\s+\d+\s+min|jaldi|abhi\s+transfer|taratari|suspended\s+in\s+\d+\s+hours?)",
        re.IGNORECASE,
    )
    POOL_PATTERNS = re.compile(
        r"(vip\s+group|insider\s+pool|operator\s+setting|institutional\s+pool|collective\s+fund|pool\s+trading)",
        re.IGNORECASE,
    )

    def __init__(self):
        self.sebi_auditor = SebiRegistryAuditor()
        self.payment_auditor = PaymentChannelAuditor()
        self.domain_auditor = DomainAuditor()

    def evaluate(self, text: str, claimed_entity_name: str | None = None) -> ThreatReport:
        # Run symbolic sub-engines
        sebi_res = self.sebi_auditor.audit_registration(text, claimed_name=claimed_entity_name)
        payment_res = self.payment_auditor.audit_payment(text)
        domain_res = self.domain_auditor.audit_domains(text)

        # Audit psychological & illegal scheme invariants
        has_guaranteed_returns = bool(self.GUARANTEED_PATTERNS.search(text))
        has_urgency = bool(self.URGENCY_PATTERNS.search(text))
        has_pool = bool(self.POOL_PATTERNS.search(text))

        # Calculate penalty weights
        penalties: dict[str, int] = {}
        violations: list[str] = []

        if has_guaranteed_returns:
            penalties["GUARANTEED_RETURNS_CLAIM"] = 35
            violations.append(
                "Violation of Regulation 15(1) of SEBI (Research Analysts) Regulations, 2014 & SEBI Master Circular (Strict prohibition on promising fixed/assured returns)"
            )

        if sebi_res.penalty_points > 0:
            label = "SEBI_SPOOF_IMPERSONATION" if sebi_res.is_impersonation_suspected else "SEBI_REGISTRATION_ANOMALY"
            penalties[label] = sebi_res.penalty_points
            if sebi_res.statutory_violation:
                violations.append(sebi_res.statutory_violation)

        if payment_res.penalty_points > 0:
            penalties["PERSONAL_UPI_PAYMENT_COLLECTION"] = payment_res.penalty_points
            if payment_res.statutory_violation:
                violations.append(payment_res.statutory_violation)

        if domain_res.penalty_points > 0:
            penalties["DECEPTIVE_DOMAIN_OR_APK"] = domain_res.penalty_points
            if domain_res.statutory_violation:
                violations.append(domain_res.statutory_violation)

        if has_urgency:
            penalties["ARTIFICIAL_URGENCY_FOMO"] = 15

        if has_pool:
            penalties["UNREGISTERED_POOL_OR_COLLECTIVE_SCHEME"] = 35
            violations.append(
                "Section 11AA SEBI Act 1992 (Prohibition on Unregistered Collective Investment Schemes / Syndicate Pooling)"
            )

        # Evaluate Red Line Overrides
        red_line = False
        red_line_reason = None

        if domain_res.has_apk_link:
            red_line = True
            red_line_reason = "Malicious or Unofficial APK Trading Terminal link detected. Immediate Critical Threat."
        elif sebi_res.is_impersonation_suspected and payment_res.is_personal_vpa:
            red_line = True
            red_line_reason = "Spoofing of licensed SEBI entity combined with unauthorized personal UPI fee diversion."
        elif has_guaranteed_returns and payment_res.is_personal_vpa:
            red_line = True
            red_line_reason = "Guaranteed return promises combined with personal UPI transfer destination constitutes prima facie criminal deceit."

        # Compute composite threat score
        raw_score = sum(penalties.values())
        if red_line:
            composite_score = 100
        else:
            composite_score = min(100, raw_score)

        # Categorize severity
        if composite_score <= 24:
            severity = "LOW_RISK"
        elif composite_score <= 59:
            severity = "MODERATE_CAUTION"
        elif composite_score <= 84:
            severity = "HIGH_THREAT"
        else:
            severity = "CRITICAL_FRAUD"

        # Determine Institutional Grievance Routing
        if sebi_res.is_in_registry and (sebi_res.is_impersonation_suspected or has_guaranteed_returns):
            recommended_routing = "SEBI_SCORES_2_0"
        elif composite_score >= 60:
            recommended_routing = "NCRP_1930_AND_SEBI_MI"
        else:
            recommended_routing = "VERIFIED_NO_ACTION_REQUIRED"

        # Build Plain summaries
        en_summary, hi_summary, bn_summary = self._generate_summaries(
            severity=severity,
            has_guaranteed=has_guaranteed_returns,
            is_personal_vpa=payment_res.is_personal_vpa,
            has_apk=domain_res.has_apk_link,
            is_typo=domain_res.is_typosquatted,
            sebi_res=sebi_res,
            routing=recommended_routing,
        )

        return ThreatReport(
            composite_threat_score=composite_score,
            severity=severity,
            guaranteed_returns_detected=has_guaranteed_returns,
            urgency_fomo_detected=has_urgency,
            unregistered_pool_detected=has_pool,
            red_line_triggered=red_line,
            red_line_reason=red_line_reason,
            sebi_audit=sebi_res,
            payment_audit=payment_res,
            domain_audit=domain_res,
            statutory_violations=violations,
            penalty_breakdown=penalties,
            recommended_routing=recommended_routing,
            plain_english_summary=en_summary,
            vernacular_hindi_summary=hi_summary,
            vernacular_bengali_summary=bn_summary,
        )

    def _generate_summaries(
        self, severity, has_guaranteed, is_personal_vpa, has_apk, is_typo, sebi_res, routing
    ):
        if severity == "LOW_RISK":
            en = "This communication matches verified regulatory invariants. No guaranteed returns or unsafe personal payment channels were found."
            hi = "यह संदेश SEBI के आधिकारिक नियमों के अनुकूल है। इसमें कोई गैरकानूनी गारंटी या व्यक्तिगत UPI खाता नहीं पाया गया।"
            bn = "এই বার্তাটি সেবির নিয়ম মেনে তৈরি। কোনো অবৈধ গ্যারান্টি বা ব্যক্তিগত ইউপিআই অ্যাকাউন্ট পাওয়া যায়নি।"
            return en, hi, bn

        en_reasons = []
        hi_reasons = []
        bn_reasons = []

        if has_guaranteed:
            en_reasons.append("promises illegal guaranteed/fixed profits (banned by SEBI)")
            hi_reasons.append("अवैध गारंटीड मुनाफे का लालच दिया जा रहा है")
            bn_reasons.append("অবৈধ নিশ্চিত লাভের লোভ দেখানো হচ্ছে")

        if is_personal_vpa:
            en_reasons.append("demands money into a private individual's UPI account")
            hi_reasons.append("पैसे किसी निजी व्यक्ति के पर्सनल UPI पर मांगे जा रहे हैं")
            bn_reasons.append("টাকা কোনো বেসরকারি ব্যক্তির ব্যক্তিগত ইউপিআইতে চাওয়া হচ্ছে")

        if has_apk:
            en_reasons.append("promotes an unofficial APK app (malware hazard)")
            hi_reasons.append("अनधिकृत APK ऐप डाउनलोड करने को कहा जा रहा है")
            bn_reasons.append("অননুমোদিত এপিকে অ্যাপ ডাউনলোড করতে বলা হচ্ছে")

        if is_typo:
            en_reasons.append("links to a deceptive clone website")
            hi_reasons.append("नकली या मिलती-जुलती फर्जी वेबसाइट का लिंक दिया गया है")
            bn_reasons.append("নকল বা জাল ওয়েবসাইটের লিংক দেওয়া হয়েছে")

        en_joined = "; ".join(en_reasons) if en_reasons else "suspicious unregulated solicitation detected"
        hi_joined = "; ".join(hi_reasons) if hi_reasons else "संदेहास्पद गतिविधि पाई गई"
        bn_joined = "; ".join(bn_reasons) if bn_reasons else "সন্দেহজনক কার্যকলাপ ধরা পড়েছে"

        en = f"ALERT: High fraud risk ({severity}). This message {en_joined}. Do NOT transfer any money."
        hi = f"सतर्क रहें! यह गंभीर धोखाधड़ी हो सकती है। इसमें {hi_joined}। किसी भी खाते में पैसे न भेजें।"
        bn = f"সতর্ক থাকুন! এটি একটি গুরুতর জালিয়াতি হতে পারে। এতে {bn_joined}। কোনো টাকা পাঠাবেন না।"

        return en, hi, bn
