"""Regulatory Jurisdictional Router: SEBI SCORES 2.0 vs SEBI MI vs NCRP 1930."""

from dataclasses import dataclass

from satark_bharat.decision.threat_engine import ThreatReport


@dataclass
class JurisdictionalRoute:
    portal_name: str
    portal_url: str
    target_authority: str
    statutory_basis: str
    routing_rationale: str
    dossier_type: str


class RegulatoryRouter:
    @staticmethod
    def resolve_route(report: ThreatReport) -> JurisdictionalRoute:
        # Route 1: Registered Intermediary Misconduct / Impersonation -> SCORES 2.0
        if report.sebi_audit.is_in_registry:
            return JurisdictionalRoute(
                portal_name="SEBI SCORES 2.0 Portal",
                portal_url="https://scores.sebi.gov.in/",
                target_authority="Securities and Exchange Board of India (Intermediary Supervision)",
                statutory_basis="SEBI (Intermediary) Regulations & SEBI Complaint Redress System (SCORES) Mandate",
                routing_rationale="Respondent claims an authentic SEBI Intermediary Registration ID present on the master register. Under SCORES 2.0 guidelines, complaints involving registered entities must be submitted directly to SCORES with intermediary cross-referencing.",
                dossier_type="SEBI_SCORES_2_0_INTERMEDIARY_DOCKET",
            )

        # Route 2: Unregistered Criminal Fraud / Telegram Syndicate / Malicious APK -> NCRP 1930 & SEBI MI
        if report.composite_threat_score >= 60:
            return JurisdictionalRoute(
                portal_name="NCRP (National Cyber Crime Reporting Portal) + SEBI Market Intelligence",
                portal_url="https://cybercrime.gov.in/",
                target_authority="Indian Cyber Crime Coordination Centre (I4C) / MHA & SEBI MI Cell",
                statutory_basis="Section 66D Information Technology Act 2000 & BNS Section 318(4) (Cheating by Personation)",
                routing_rationale="Entity is completely unregistered with SEBI, operating an illegal money-pooling syndicate or distributing malicious APKs. SCORES 2.0 rejects unregistered respondents; immediate jurisdictional action belongs to NCRP/1930 for bank/VPA account freezing and SEBI MI for search & seizure.",
                dossier_type="NCRP_CYBERCRIME_AND_SEBI_MI_DOCKET",
            )

        # Route 3: Verified / Low Risk
        return JurisdictionalRoute(
            portal_name="No Regulatory Filing Required",
            portal_url="https://sebi.gov.in",
            target_authority="N/A",
            statutory_basis="Compliant with SEBI Intermediary Norms",
            routing_rationale="No statutory violations detected. Entity and communication match verified regulatory standards.",
            dossier_type="VERIFIED_AUDIT_LOG",
        )
