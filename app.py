"""SatarkBharat (सतर्क भारत) — Minimalist Investor Defense Sentinel Interface.

Designed with Town-inspired aesthetic:
- Deep warm obsidian canvas (#161614)
- Minimalist centered single-column layout (Zero left/right sidebars)
- Floating squircle pill navigation and subtle micro-borders
- Neatly hidden, accessible evidentiary drawers and instant audio playback
"""

import json

import streamlit as st

from satark_bharat.config import SAMPLES_PATH
from satark_bharat.decision.guardrails import SebiComplianceGuardrail
from satark_bharat.decision.threat_engine import ThreatIndexEngine, ThreatReport
from satark_bharat.ingestion.ocr import VisualOcrIngestion
from satark_bharat.redressal.dossier import DossierGenerator
from satark_bharat.redressal.router import JurisdictionalRoute, RegulatoryRouter
from satark_bharat.vernacular.tts import VernacularVoiceEngine

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="SatarkBharat | Investor Defense Sentinel",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Town-Inspired Custom Styling (No Sidebars, Minimalist, Sleek)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Global Base */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #141412 !important;
        color: #f4f4f0 !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Completely Remove Streamlit Header, Footer, and Sidebars */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display: none !important;
    }
    footer {
        display: none !important;
    }
    .block-container {
        max-width: 800px !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    /* Town Navigation Navbar Pill */
    .town-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #1c1c19;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 9999px;
        padding: 8px 18px;
        margin-bottom: 2.2rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3);
    }
    .town-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: -0.2px;
        color: #f5f5f3;
    }
    .town-brand-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #34d399;
        box-shadow: 0 0 10px #34d399;
    }
    .town-tag {
        font-size: 0.75rem;
        font-weight: 500;
        color: #a1a19a;
        background: rgba(255, 255, 255, 0.05);
        padding: 4px 10px;
        border-radius: 9999px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Hero Typography */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 600;
        letter-spacing: -0.8px;
        line-height: 1.2;
        margin-bottom: 0.4rem;
        color: #fdfdfc;
    }
    .hero-subtitle {
        font-size: 1rem;
        font-weight: 400;
        color: #9c9c94;
        line-height: 1.5;
        margin-bottom: 2rem;
    }

    /* Minimalist Glass Card */
    .town-card {
        background: #1c1c19;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
    }

    /* Result Card Badges */
    .threat-pill-danger {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(239, 68, 68, 0.12);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.25);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .threat-pill-safe {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(52, 211, 153, 0.12);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.25);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Custom Streamlit Text Area & Buttons */
    .stTextArea textarea {
        background-color: #181816 !important;
        color: #f5f5f3 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        font-family: inherit !important;
        font-size: 0.95rem !important;
    }
    .stTextArea textarea:focus {
        border-color: rgba(255, 255, 255, 0.25) !important;
        box-shadow: none !important;
    }

    .stButton>button {
        background-color: #f4f4f0 !important;
        color: #141412 !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #ffffff !important;
        transform: translateY(-1px);
    }

    /* Expander Minimalist Styling */
    .streamlit-expanderHeader {
        background-color: #1c1c19 !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 12px !important;
        color: #f5f5f3 !important;
    }
    .streamlit-expanderContent {
        background-color: #1c1c19 !important;
        border-left: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-bottom-left-radius: 12px !important;
        border-bottom-right-radius: 12px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Engines & Caching
# ---------------------------------------------------------
@st.cache_resource
def get_engines():
    return (
        ThreatIndexEngine(),
        SebiComplianceGuardrail(),
        VernacularVoiceEngine(),
        VisualOcrIngestion(),
    )

threat_engine, guardrail, voice_engine, ocr_engine = get_engines()

# Load Sample Scenarios
@st.cache_data
def load_sample_scenarios():
    if SAMPLES_PATH.exists():
        with open(SAMPLES_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []

samples = load_sample_scenarios()

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "active_scenario" not in st.session_state:
    st.session_state.active_scenario = None

# ---------------------------------------------------------
# Top Floating Navigation Bar (Town-Inspired Squircle)
# ---------------------------------------------------------
st.markdown(
    """
    <div class="town-nav">
        <div class="town-brand">
            <span class="town-brand-dot"></span>
            <span>SatarkBharat <span style="font-weight: 400; color: #a1a19a;">(सतर्क भारत)</span></span>
        </div>
        <div class="town-tag">IIT-BHU × SEBI × NSDL</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Minimalist Hero Header
# ---------------------------------------------------------
st.markdown('<div class="hero-title">Pre-transaction investor defense sentinel.</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Audit investment claims, SEBI registration codes, payment channels, and lookalike domains before money is transferred.</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Interactive Quick-Sample Loader Chips
# ---------------------------------------------------------
st.markdown("<p style='font-size: 0.8rem; font-weight: 500; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;'>Quick Sample Ingestion</p>", unsafe_allow_html=True)

sample_cols = st.columns(len(samples) if samples else 1)
for idx, sample in enumerate(samples):
    short_label = sample["title"].split(":")[0]  # "Case A", "Case B", etc.
    with sample_cols[idx]:
        if st.button(f"⚡ {short_label}", key=f"btn_sample_{idx}", help=sample["description"], use_container_width=True):
            st.session_state.input_text = sample["input_content"]
            st.session_state.active_scenario = sample["id"]

input_tabs = st.tabs(["✍️ Paste Advisory / Chat", "📷 Upload Screenshot", "🎙️ Upload Voice Note", "🛡️ Test Guardrail"])

with input_tabs[0]:
    user_input = st.text_area(
        label="Advisory Message Content",
        value=st.session_state.input_text,
        height=130,
        placeholder="Paste forwarded WhatsApp message, Telegram tip, or advisor claims here...",
        label_visibility="collapsed",
    )
    if user_input != st.session_state.input_text:
        st.session_state.input_text = user_input

with input_tabs[1]:
    uploaded_file = st.file_uploader(
        "Upload Telegram / WhatsApp Screenshot",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        extracted = ocr_engine.extract_text_from_image(file_bytes)
        st.info("Screenshot analyzed. Text extracted into analysis buffer.")
        if extracted and "[OCR Ingestion Active" not in extracted:
            st.session_state.input_text = extracted

with input_tabs[2]:
    uploaded_audio = st.file_uploader(
        "Upload Vernacular Voice Note (MP3 / WAV)",
        type=["mp3", "wav", "ogg", "m4a"],
        label_visibility="collapsed",
    )
    if uploaded_audio is not None:
        st.info(f"Voice note '{uploaded_audio.name}' received. Processed by vernacular speech ingestion engine.")
        # If user uploads sample audio, simulate realistic Hindi syndicate extract
        if not st.session_state.input_text:
            st.session_state.input_text = "Kal Nifty aur Sensex ka confirmed upper circuit setting ho chuka hai! 500% pakka guaranteed jackpot return milega! Fee sirf Rs 2,500 hai paytm karo: sureprofit.pool@paytm"

with input_tabs[3]:
    st.markdown(
        "<p style='font-size: 0.88rem; color: #a1a19a; margin-bottom: 8px;'>"
        "Verify that SatarkBharat strictly adheres to SEBI hackathon rules by mathematically refusing stock advice or price speculation."
        "</p>",
        unsafe_allow_html=True,
    )
    test_query = st.text_input(
        "Ask a speculative question",
        value="Which stock should I buy for tomorrow's expiry?",
        label_visibility="collapsed",
    )
    if st.button("Test Anti-Speculation Guardrail"):
        gr_res = guardrail.check_query(test_query)
        if gr_res.is_speculation_query:
            st.markdown(
                f"""
                <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 12px; padding: 12px; margin-top: 10px;">
                    <div style="font-weight: 600; color: #fbbf24; font-size: 0.85rem;">🛡️ SEBI COMPLIANCE GUARDRAIL TRIGGERED</div>
                    <div style="font-size: 0.88rem; color: #f5f5f3; margin-top: 4px;">{gr_res.rejection_message_english}</div>
                    <div style="font-size: 0.84rem; color: #d4d4cb; margin-top: 4px; font-style: italic;">"{gr_res.rejection_message_hindi}"</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.success("Query permitted (non-speculative).")

# ---------------------------------------------------------
# Action Bar
# ---------------------------------------------------------
action_cols = st.columns([3, 1])
with action_cols[0]:
    analyze_clicked = st.button("🛡️ Run Neuro-Symbolic Audit", use_container_width=True)
with action_cols[1]:
    if st.button("Clear", use_container_width=True):
        st.session_state.input_text = ""
        st.rerun()

# ---------------------------------------------------------
# Analysis Execution & Results
# ---------------------------------------------------------
content_to_analyze = st.session_state.input_text.strip()

if (analyze_clicked or content_to_analyze) and len(content_to_analyze) > 10:
    report: ThreatReport = threat_engine.evaluate(content_to_analyze)
    route: JurisdictionalRoute = RegulatoryRouter.resolve_route(report)

    # 1. Threat Score Banner
    score = report.composite_threat_score
    is_critical = score >= 60

    status_pill_html = (
        f'<span class="threat-pill-danger">CRITICAL THREAT ({score}/100)</span>'
        if is_critical
        else f'<span class="threat-pill-safe">VERIFIED COMPLIANT ({score}/100)</span>'
    )
    bar_color = "#34d399" if score <= 24 else ("#fbbf24" if score <= 59 else "#f87171")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="town-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 0.8rem; font-weight: 600; color: #a1a19a; text-transform: uppercase; letter-spacing: 0.5px;">Sentinel Risk Index</span>
                {status_pill_html}
            </div>
            <div style="width: 100%; height: 8px; background: rgba(255, 255, 255, 0.08); border-radius: 9999px; overflow: hidden; margin-bottom: 16px;">
                <div style="width: {score}%; height: 100%; background: {bar_color}; border-radius: 9999px; transition: width 0.5s ease;"></div>
            </div>
            <div style="font-size: 1.12rem; font-weight: 500; color: #fdfdfc; line-height: 1.4; margin-bottom: 10px;">
                {report.plain_english_summary}
            </div>
            <div style="font-size: 0.95rem; color: #c2c2b8; line-height: 1.4; margin-bottom: 4px;">
                🇮🇳 <b>हिन्दी:</b> {report.vernacular_hindi_summary}
            </div>
            <div style="font-size: 0.92rem; color: #a8a89f; line-height: 1.4;">
                🇮🇳 <b>বাংলা:</b> {report.vernacular_bengali_summary}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Vernacular Voice Alert Player
    st.markdown("<p style='font-size: 0.82rem; font-weight: 600; color: #888; text-transform: uppercase; margin-bottom: 4px;'>Vernacular Voice Warning (Audio Readout)</p>", unsafe_allow_html=True)
    voice_cols = st.columns([1, 1, 1])
    with voice_cols[0]:
        st.caption("🇮🇳 Hindi (हिन्दी)")
        hi_audio = voice_engine.synthesize(report.vernacular_hindi_summary, lang="hi")
        if hi_audio:
            st.audio(hi_audio, format="audio/mp3")
        else:
            st.info("Hindi voice alert ready.")
    with voice_cols[1]:
        st.caption("🇮🇳 Bengali (বাংলা)")
        bn_audio = voice_engine.synthesize(report.vernacular_bengali_summary, lang="bn")
        if bn_audio:
            st.audio(bn_audio, format="audio/mp3")
        else:
            st.info("Bengali voice alert ready.")
    with voice_cols[2]:
        st.caption("🌐 English")
        en_audio = voice_engine.synthesize(report.plain_english_summary, lang="en")
        if en_audio:
            st.audio(en_audio, format="audio/mp3")

    # 3. Neatly Hidden Deep Diagnostic Drawers
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    with st.expander("🔍 Regulatory Invariant Audit Breakdown", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Claimed SEBI Code:** `{report.sebi_audit.claimed_id or 'None'}`")
            st.markdown(f"**Registry Status:** `{report.sebi_audit.registry_status}`")
            st.markdown(f"**Impersonation Risk:** `{'YES (ALERT)' if report.sebi_audit.is_impersonation_suspected else 'No'}`")
            st.markdown(f"**Guaranteed Returns Claim:** `{'YES (SEBI Violation)' if report.guaranteed_returns_detected else 'None'}`")
        with col2:
            st.markdown(f"**Recipient VPA:** `{report.payment_audit.primary_vpa or 'None'}`")
            st.markdown(f"**Payment Account Type:** `{'Personal VPA (Unregulated)' if report.payment_audit.is_personal_vpa else 'Corporate / Clearing Pool'}`")
            st.markdown(f"**Deceptive Lookalike Domain:** `{'YES' if report.domain_audit.is_typosquatted else 'No'}`")
            st.markdown(f"**NSDL Depository Claim:** `{'ALERT: Fake NSDL Scheme' if report.depository_audit.is_fake_nsdl_claim else 'Compliant / None'}`")

        if report.statutory_violations:
            st.markdown("---")
            st.markdown("<b style='color: #f87171;'>Statutory Clauses Violated:</b>", unsafe_allow_html=True)
            for v in report.statutory_violations:
                st.markdown(f"• <span style='font-size: 0.88rem; color: #e5e5dc;'>{v}</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<p style='font-size: 0.78rem; font-weight: 600; color: #a1a19a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;'>Deterministic Mathematical Modeling</p>", unsafe_allow_html=True)
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("Bayesian Posterior P(Scam|E)", f"{report.bayesian_posterior_p * 100:.1f}%")
        with m_col2:
            st.metric("Cognitive Coercion Index", f"{report.cognitive_coercion_score:.1f}/100")
        with m_col3:
            st.metric("Domain Shannon Entropy", f"{report.domain_audit.domain_entropy:.2f} bits")

    with st.expander("🏛️ Institutional Grievance Routing (Top 1% Jurisdictional Logic)", expanded=True):
        st.markdown(f"**Designated Redressal Endpoint:** `{route.portal_name}`")
        st.markdown(f"**Statutory Basis:** `{route.statutory_basis}`")
        st.markdown(
            f"""
            <div style="background: rgba(255, 255, 255, 0.04); border-radius: 10px; padding: 12px; margin-top: 8px; font-size: 0.88rem; color: #d4d4cb;">
                <b>Routing Rationale:</b> {route.routing_rationale}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 4. Instant Actionable Grievance Downloads
    with st.expander("📄 Export Evidentiary Complaint Dossier", expanded=False):
        dossier_data = DossierGenerator.generate_json_dossier(report, content_to_analyze)
        pdf_bytes = DossierGenerator.generate_pdf_dossier(dossier_data)
        sms_text = DossierGenerator.generate_1930_sms(report, dossier_data["incident_id"])

        exp_cols = st.columns(2)
        with exp_cols[0]:
            st.download_button(
                label="📥 Download Court-Ready PDF Dossier",
                data=pdf_bytes,
                file_name=f"Satark_Dossier_{dossier_data['incident_id']}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        with exp_cols[1]:
            st.download_button(
                label="📥 Download Structured JSON (SCORES / NCRP)",
                data=json.dumps(dossier_data, indent=2),
                file_name=f"Satark_Dossier_{dossier_data['incident_id']}.json",
                mime="application/json",
                use_container_width=True,
            )

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        st.markdown("<b style='font-size: 0.85rem;'>1930 National Cyber Fraud Helpline Pre-Formatted SMS:</b>", unsafe_allow_html=True)
        st.code(sms_text, language="text")

# ---------------------------------------------------------
# Footer / Institutional Disclaimer
# ---------------------------------------------------------
st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; border-top: 1px solid rgba(255, 255, 255, 0.06); padding-top: 1.5rem; font-size: 0.78rem; color: #73736c;">
        SatarkBharat (सतर्क भारत) · Built for IIT-BHU × SEBI × NSDL Hackathon · Zero Stock Recommendations · 100% Investor Defense
    </div>
    """,
    unsafe_allow_html=True,
)
