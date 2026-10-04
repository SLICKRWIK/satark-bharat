"""Unit and integration test suite for SatarkBharat Symbolic & Redressal Engines."""

from satark_bharat.decision.guardrails import SebiComplianceGuardrail
from satark_bharat.decision.threat_engine import ThreatIndexEngine
from satark_bharat.redressal.dossier import DossierGenerator
from satark_bharat.symbolic.domain_auditor import DomainAuditor
from satark_bharat.symbolic.payment_auditor import PaymentChannelAuditor
from satark_bharat.symbolic.sebi_registry import SebiRegistryAuditor


def test_sebi_registry_valid_research_analyst():
    auditor = SebiRegistryAuditor()
    text = "We are Apex Capital Research, SEBI Reg: INH000008921. Guaranteed profits!"
    result = auditor.audit_registration(text, claimed_name="Apex Capital Advisors LLP")
    assert result.claimed_id == "INH000008921"
    assert result.is_valid_format is True
    assert result.category == "RESEARCH_ANALYST"
    assert result.is_in_registry is True
    assert result.registry_status == "VERIFIED_ACTIVE"
    assert result.is_impersonation_suspected is False


def test_sebi_registry_unregistered_missing():
    auditor = SebiRegistryAuditor()
    text = "Join our Telegram channel for 500% profit. Send money to 9876543210@paytm."
    result = auditor.audit_registration(text)
    assert result.claimed_id is None
    assert result.is_in_registry is False
    assert result.registry_status == "NONE_CLAIMED"
    assert result.penalty_points == 30


def test_payment_auditor_personal_vpa():
    auditor = PaymentChannelAuditor()
    text = "Send your advisory fees to rajesh.kumar99@okhdfcbank to get immediate VIP access."
    result = auditor.audit_payment(text)
    assert result.primary_vpa == "rajesh.kumar99@okhdfcbank"
    assert result.is_personal_vpa is True
    assert result.is_clearing_compliant is False
    assert result.penalty_points == 25


def test_payment_auditor_corporate_merchant():
    auditor = PaymentChannelAuditor()
    text = "Please deposit account maintenance margin to zerodha@hdfcbank."
    result = auditor.audit_payment(text)
    assert result.is_personal_vpa is False
    assert result.is_clearing_compliant is True
    assert result.penalty_points == 0


def test_domain_auditor_typosquatting_and_apk():
    auditor = DomainAuditor()
    text = "Download Zerodha Pro terminal: https://zer0dha-app.trade/login.apk"
    result = auditor.audit_domains(text)
    assert result.has_apk_link is True
    assert result.is_typosquatted is True
    assert result.spoofed_target == "zerodha.com"
    assert result.penalty_points == 40


def test_threat_engine_scenario_a():
    engine = ThreatIndexEngine()
    text = (
        "Namaste Sir! This is Apex Capital Research (SEBI Reg: INH000008921). "
        "Today's BankNifty Expiry jackpot: 200% GUARANTEED RETURN! Pay to rajesh.advisory99@okhdfcbank"
    )
    report = engine.evaluate(text)
    assert report.composite_threat_score >= 85
    assert report.guaranteed_returns_detected is True
    assert report.payment_audit.is_personal_vpa is True
    assert report.recommended_routing == "SEBI_SCORES_2_0"


def test_threat_engine_scenario_b_unregistered_telegram():
    engine = ThreatIndexEngine()
    text = "Kal Nifty 1000 point upar! 500% pakka guaranteed return! Paytm karo: sureprofit.pool@paytm"
    report = engine.evaluate(text)
    assert report.composite_threat_score >= 85
    assert report.recommended_routing == "NCRP_1930_AND_SEBI_MI"


def test_guardrail_blocks_stock_picking():
    guardrail = SebiComplianceGuardrail()
    result = guardrail.check_query("Which stock should I buy for tomorrow's expiry?")
    assert result.is_speculation_query is True
    assert result.blocked_intent == "STOCK_PICKING_REQUEST"
    assert "SEBI" in result.rejection_message_english


def test_dossier_pdf_generation():
    engine = ThreatIndexEngine()
    text = "Kal 100% guaranteed jackpot return! Send money to scammer@ybl"
    report = engine.evaluate(text)
    dossier_data = DossierGenerator.generate_json_dossier(report, text)
    pdf_bytes = DossierGenerator.generate_pdf_dossier(dossier_data)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")


def test_vernacular_hindi_and_bengali_summaries():
    engine = ThreatIndexEngine()
    text = "Kal 100% guaranteed jackpot return! Send money to scammer@ybl"
    report = engine.evaluate(text)
    assert len(report.vernacular_hindi_summary) > 10
    assert len(report.vernacular_bengali_summary) > 10
    assert "सतर्क" in report.vernacular_hindi_summary
    assert "সতর্ক" in report.vernacular_bengali_summary


def test_nsdl_depository_auditor():
    from satark_bharat.symbolic.nsdl_auditor import NsdlDepositoryAuditor
    auditor = NsdlDepositoryAuditor()
    scam_text = "Urgent: Pay Rs 10,000 to avoid NSDL freeze notice on your demat account IN30012345678901."
    res = auditor.audit_depository_claims(scam_text)
    assert res.is_fake_nsdl_claim is True
    assert res.depository_type == "NSDL"
    assert res.penalty_points == 35


def test_advanced_deterministic_math():
    from satark_bharat.decision.math_engine import (
        BayesianEvidenceFusion,
        compute_cognitive_coercion_index,
        weighted_damerau_levenshtein,
    )

    # 1. Homoglyph cost check (0 vs o should be distance ~0.25 rather than 1.0)
    dist = weighted_damerau_levenshtein("zer0dha", "zerodha")
    assert dist < 0.5

    # 2. Cognitive coercion saturation curve
    c0 = compute_cognitive_coercion_index(0)
    c3 = compute_cognitive_coercion_index(3)
    assert c0 == 0.0
    assert c3 > 75.0

    # 3. Bayesian evidence fusion
    fusion = BayesianEvidenceFusion.fuse_evidence(["GUARANTEED_RETURNS_CLAIM", "PERSONAL_UPI_VPA"])
    assert fusion.posterior_probability > 0.95
    assert fusion.confidence_level in ("VERY_HIGH", "DEFINITIVE_RED_LINE")


def test_sebi_registry_non_financial_text_zero_penalty():
    auditor = SebiRegistryAuditor()
    result = auditor.audit_registration("hello man")
    assert result.claimed_id is None
    assert result.penalty_points == 0
    assert result.registry_status == "NOT_APPLICABLE"
    assert result.statutory_violation is None


def test_guardrail_blocks_recommendation_variations():
    guardrail = SebiComplianceGuardrail()

    test_queries = [
        "can you recommend a stock for tomorrow?",
        "can you recommend me some stocks for tommorwo?",
        "bhai kal konsa share lu?",
        "kisme invest kare batao?",
        "give me intraday tips",
    ]

    for q in test_queries:
        res = guardrail.check_query(q)
        assert res.is_speculation_query is True, f"Guardrail failed to block: '{q}'"
        assert "SEBI" in res.rejection_message_english



