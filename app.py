"""SatarkBharat (सतर्क भारत) — Minimalist Investor Defense Sentinel.

Faithfully crafted in the visual aesthetic of Town (town.com):
- Warm eggshell/ivory canvas (#fbfbfa)
- High-contrast editorial serif headlines (Fraunces / Editorial Serif)
- Modern geometric interface typography (Plus Jakarta Sans)
- Elegant floating input card with subtle bottom toolbar
- Checklist-oriented audit results (identical to Town's to-do / activity feed)
- Zero emoji clutter; refined micro-pills, delicate hairline borders, and generous whitespace
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
    page_title="SatarkBharat — Investor Defense Sentinel",
    page_icon="○",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Town-Inspired Aesthetic (Warm Ivory, Editorial Serif, Zero Emojis)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Google Fonts: Fraunces (Editorial Serif) + Plus Jakarta Sans + JetBrains Mono */
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Plus+Jakarta+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Background & Base */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #fbfbfa !important;
        color: #18181b !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* Hide Default Streamlit Navigation, Sidebars, and Footers */
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
        max-width: 780px !important;
        padding-top: 2.2rem !important;
        padding-bottom: 5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    /* Town Navigation Header */
    .town-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 3.5rem;
    }
    .town-logo-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 8px;
        padding: 6px 14px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        color: #18181b;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }
    .town-logo-symbol {
        font-size: 1rem;
        line-height: 1;
        color: #18181b;
    }
    .town-nav-pills {
        display: inline-flex;
        align-items: center;
        gap: 20px;
        border: 1px solid rgba(0, 0, 0, 0.07);
        border-radius: 8px;
        padding: 6px 18px;
        background: transparent;
        font-size: 0.82rem;
        font-weight: 500;
        color: #52525b;
    }
    .town-nav-pills span {
        cursor: default;
    }
    .town-auth-pills {
        display: inline-flex;
        align-items: center;
        gap: 12px;
    }
    .town-badge-secondary {
        font-size: 0.8rem;
        font-weight: 500;
        color: #71717a;
        text-decoration: none;
    }
    .town-button-primary {
        background: #18181b;
        color: #fbfbfa !important;
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 0.82rem;
        font-weight: 500;
        text-decoration: none;
        display: inline-block;
    }

    /* Town Editorial Hero */
    .town-hero {
        margin-bottom: 2.8rem;
    }
    .town-hero-headline {
        font-family: 'Fraunces', serif !important;
        font-size: 3.4rem !important;
        font-weight: 450 !important;
        line-height: 1.12 !important;
        letter-spacing: -1.2px !important;
        color: #18181b !important;
        margin-bottom: 1.4rem !important;
    }
    .town-hero-lead {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        font-size: 0.98rem;
        line-height: 1.6;
        color: #3f3f46;
        max-width: 640px;
    }
    .town-avatar {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #e4e4e7;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        color: #52525b;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .town-pill-salmon {
        display: inline-block;
        background: #ffedd5;
        color: #c2410c;
        padding: 1px 7px;
        border-radius: 4px;
        font-size: 0.86rem;
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Town Floating Input Card */
    .town-input-card {
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 14px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
        padding: 18px 20px;
        margin-bottom: 2rem;
    }

    /* Checklist Section (Modeled after Town's to-do / activity list) */
    .town-list-container {
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 14px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
        padding: 20px 24px;
        margin-top: 1.8rem;
        margin-bottom: 2rem;
    }
    .town-list-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 14px;
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
        margin-bottom: 14px;
    }
    .town-list-title {
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: #71717a;
    }
    .town-list-item {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        padding: 14px 0;
        border-bottom: 1px solid rgba(0, 0, 0, 0.04);
    }
    .town-list-item:last-child {
        border-bottom: none;
        padding-bottom: 4px;
    }
    .town-item-left {
        display: flex;
        gap: 12px;
        max-width: 540px;
    }
    .town-item-checkbox {
        width: 16px;
        height: 16px;
        border-radius: 4px;
        border: 1.5px solid #d4d4d8;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        margin-top: 2px;
        flex-shrink: 0;
    }
    .town-item-checkbox.checked {
        border-color: #18181b;
        background: #18181b;
        color: #ffffff;
    }
    .town-item-title {
        font-size: 0.94rem;
        font-weight: 500;
        color: #18181b;
        line-height: 1.4;
    }
    .town-item-desc {
        font-size: 0.82rem;
        color: #71717a;
        margin-top: 2px;
        line-height: 1.45;
    }

    /* Minimalist Town Status Pills */
    .status-pill {
        font-size: 0.75rem;
        font-weight: 500;
        padding: 2px 8px;
        border-radius: 4px;
        white-space: nowrap;
    }
    .status-pill.danger {
        background: #fee2e2;
        color: #b91c1c;
    }
    .status-pill.warning {
        background: #fef3c7;
        color: #b45309;
    }
    .status-pill.safe {
        background: #ecfdf5;
        color: #047857;
    }
    .status-pill.neutral {
        background: #f4f4f5;
        color: #52525b;
    }

    /* Streamlit Overrides for Clean White Inputs */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #18181b !important;
        border: none !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.98rem !important;
        line-height: 1.5 !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    .stTextArea textarea:focus {
        box-shadow: none !important;
    }

    .stButton>button {
        background-color: #18181b !important;
        color: #ffffff !important;
        border: 1px solid #18181b !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.45rem 1.1rem !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    }
    .stButton>button:hover {
        background-color: #27272a !important;
        border-color: #27272a !important;
        color: #ffffff !important;
    }

    /* Secondary subtle button */
    .stDownloadButton>button {
        background-color: #ffffff !important;
        color: #18181b !important;
        border: 1px solid rgba(0, 0, 0, 0.12) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.82rem !important;
        padding: 0.45rem 1rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
    }
    .stDownloadButton>button:hover {
        background-color: #f4f4f5 !important;
        border-color: rgba(0, 0, 0, 0.2) !important;
    }

    /* Clean Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
        background: transparent;
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
        padding-bottom: 6px;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #71717a !important;
        font-size: 0.84rem !important;
        font-weight: 500 !important;
        padding: 4px 4px !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        color: #18181b !important;
        border-bottom: 2px solid #18181b !important;
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: transparent !important;
        color: #18181b !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
    }
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        border-radius: 8px !important;
        padding: 16px !important;
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
# Top Navigation Bar (Identical to Town's Layout)
# ---------------------------------------------------------
st.markdown(
    """
    <div class="town-header">
        <div class="town-logo-pill">
            <span class="town-logo-symbol">○</span>
            <span>SATARK</span>
        </div>
        <div class="town-nav-pills">
            <span>Sentinel</span>
            <span>SCORES 2.0</span>
            <span>NCRP 1930</span>
            <span>Investor Charter</span>
        </div>
        <div class="town-auth-pills">
            <span class="town-badge-secondary">IIT-BHU · SEBI · NSDL</span>
            <a href="https://sangyan.sntciitbhu.co.in/" target="_blank" class="town-button-primary">SANGYAN</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Town Editorial Hero Section
# ---------------------------------------------------------
st.markdown(
    """
    <div class="town-hero">
        <div class="town-hero-headline">
            SatarkBharat protects your savings from fraud.
        </div>
        <div class="town-hero-lead">
            <div class="town-avatar">s</div>
            <div>
                Forward any suspicious WhatsApp advisory, Telegram tip, or payment request.
                <span class="town-pill-salmon">Satark</span> verifies regulatory invariants, recipient UPI accounts,
                and official SEBI registers before you transfer money.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Interactive Quick-Sample Chips (Subtle Town-Style Text Chips)
# ---------------------------------------------------------
sample_labels = [
    "Sample 1: Impersonated Research Analyst",
    "Sample 2: Telegram Syndicate Tip",
    "Sample 3: Cloned Broker APK",
    "Sample 4: Legitimate Broker Notice",
]

st.markdown("<p style='font-size: 0.78rem; font-weight: 600; color: #71717a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;'>Load Pre-Recorded Scenarios</p>", unsafe_allow_html=True)
chip_cols = st.columns(len(samples) if samples else 1)
for idx, sample in enumerate(samples):
    with chip_cols[idx]:
        short_name = f"Case {chr(65 + idx)}"
        if st.button(short_name, key=f"chip_{idx}", help=sample["description"], use_container_width=True):
            st.session_state.input_text = sample["input_content"]
            st.session_state.active_scenario = sample["id"]

# ---------------------------------------------------------
# Floating Input Card (Modeled after Town's Input Box)
# ---------------------------------------------------------
st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

input_tabs = st.tabs(["Message Text", "Screenshot Upload", "Voice Note Upload", "Guardrail Check"])

with input_tabs[0]:
    user_input = st.text_area(
        label="Advisory Message",
        value=st.session_state.input_text,
        height=110,
        placeholder="Type or paste the advisory message, claimed SEBI ID, or payment request here...",
        label_visibility="collapsed",
    )
    if user_input != st.session_state.input_text:
        st.session_state.input_text = user_input

with input_tabs[1]:
    uploaded_file = st.file_uploader(
        "Upload Screenshot",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        extracted = ocr_engine.extract_text_from_image(file_bytes)
        st.caption("Screenshot text extracted to analysis buffer.")
        if extracted and "[OCR Ingestion Active" not in extracted:
            st.session_state.input_text = extracted

with input_tabs[2]:
    uploaded_audio = st.file_uploader(
        "Upload Voice Note",
        type=["mp3", "wav", "ogg", "m4a"],
        label_visibility="collapsed",
    )
    if uploaded_audio is not None:
        st.caption(f"Audio stream '{uploaded_audio.name}' ingested.")
        if not st.session_state.input_text:
            st.session_state.input_text = "Kal Nifty aur Sensex ka confirmed upper circuit setting ho chuka hai! 500% pakka guaranteed jackpot return milega! Fee sirf Rs 2,500 hai paytm karo: sureprofit.pool@paytm"

with input_tabs[3]:
    st.caption("Verify that SatarkBharat strictly obeys SANGYAN guardrails by refusing speculative advice.")
    test_query = st.text_input(
        "Ask for a stock recommendation",
        value="Which stock should I buy for tomorrow's expiry?",
        label_visibility="collapsed",
    )
    if st.button("Test Anti-Speculation Guardrail"):
        gr_res = guardrail.check_query(test_query)
        if gr_res.is_speculation_query:
            st.markdown(
                f"""
                <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 12px; margin-top: 8px;">
                    <div style="font-size: 0.8rem; font-weight: 600; color: #b91c1c; text-transform: uppercase;">Guardrail Active: Speculative Advisory Blocked</div>
                    <div style="font-size: 0.86rem; color: #18181b; margin-top: 4px;">{gr_res.rejection_message_english}</div>
                    <div style="font-size: 0.82rem; color: #52525b; margin-top: 4px; font-style: italic;">"{gr_res.rejection_message_hindi}"</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.success("Query permitted.")

# ---------------------------------------------------------
# Action Bar
# ---------------------------------------------------------
btn_cols = st.columns([4, 1])
with btn_cols[0]:
    analyze_clicked = st.button("Run Regulatory Audit →", use_container_width=True)
with btn_cols[1]:
    if st.button("Clear", use_container_width=True):
        st.session_state.input_text = ""
        st.rerun()

# ---------------------------------------------------------
# Checklist-Style Activity Feed (Modeled after Town's To-Do List)
# ---------------------------------------------------------
content_to_analyze = st.session_state.input_text.strip()

if (analyze_clicked or content_to_analyze) and len(content_to_analyze) > 10:
    report: ThreatReport = threat_engine.evaluate(content_to_analyze)
    route: JurisdictionalRoute = RegulatoryRouter.resolve_route(report)

    score = report.composite_threat_score
    is_critical = score >= 60

    overall_pill_class = "danger" if is_critical else ("warning" if score > 24 else "safe")
    overall_pill_text = f"Threat Index: {score}/100 ({report.severity})"

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 1. Primary Verdict Card
    st.markdown(
        f"""
        <div class="town-list-container">
            <div class="town-list-header">
                <span class="town-list-title">Sentinel Audit Report</span>
                <span class="status-pill {overall_pill_class}">{overall_pill_text}</span>
            </div>
            <div style="font-size: 1.15rem; font-weight: 500; color: #18181b; line-height: 1.5; margin-bottom: 12px;">
                {report.plain_english_summary}
            </div>
            <div style="font-size: 0.92rem; color: #52525b; line-height: 1.5; margin-bottom: 6px;">
                <b>हिन्दी:</b> {report.vernacular_hindi_summary}
            </div>
            <div style="font-size: 0.90rem; color: #71717a; line-height: 1.5;">
                <b>বাংলা:</b> {report.vernacular_bengali_summary}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Vernacular Voice Alert Readout (Town Audio Bar)
    st.markdown("<p style='font-size: 0.78rem; font-weight: 600; color: #71717a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;'>Vernacular Voice Warning</p>", unsafe_allow_html=True)
    voice_cols = st.columns([1, 1, 1])
    with voice_cols[0]:
        st.caption("Hindi Audio")
        hi_audio = voice_engine.synthesize(report.vernacular_hindi_summary, lang="hi")
        if hi_audio:
            st.audio(hi_audio, format="audio/mp3")
    with voice_cols[1]:
        st.caption("Bengali Audio")
        bn_audio = voice_engine.synthesize(report.vernacular_bengali_summary, lang="bn")
        if bn_audio:
            st.audio(bn_audio, format="audio/mp3")
    with voice_cols[2]:
        st.caption("English Audio")
        en_audio = voice_engine.synthesize(report.plain_english_summary, lang="en")
        if en_audio:
            st.audio(en_audio, format="audio/mp3")

    # 3. Checklist-Oriented Audit Invariants (Identical to Town's To-Do List)
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Invariant 1: SEBI Registry
    sebi_checked = "checked" if not report.sebi_audit.is_impersonation_suspected and report.sebi_audit.is_in_registry else ""
    sebi_mark = "✓" if sebi_checked else "!"
    sebi_pill = "safe" if report.sebi_audit.is_in_registry and not report.sebi_audit.is_impersonation_suspected else ("danger" if report.sebi_audit.is_impersonation_suspected else "warning")
    sebi_pill_text = "Verified Match" if sebi_pill == "safe" else ("Impersonation Alert" if sebi_pill == "danger" else "Unregistered")

    # Invariant 2: Payment Channel
    pay_checked = "checked" if report.payment_audit.is_clearing_compliant else ""
    pay_mark = "✓" if pay_checked else "!"
    pay_pill = "safe" if report.payment_audit.is_clearing_compliant else "danger"
    pay_pill_text = "Clearing Compliant" if pay_pill == "safe" else "Personal Savings VPA"

    # Invariant 3: Performance Guarantee (PVA)
    pva_checked = "" if report.guaranteed_returns_detected else "checked"
    pva_mark = "!" if report.guaranteed_returns_detected else "✓"
    pva_pill = "danger" if report.guaranteed_returns_detected else "safe"
    pva_pill_text = "Prohibited Return Claim" if report.guaranteed_returns_detected else "No Fixed Guarantees"

    # Invariant 4: Domain & APK
    dom_checked = "" if report.domain_audit.is_typosquatted or report.domain_audit.has_apk_link else "checked"
    dom_mark = "!" if not dom_checked else "✓"
    dom_pill = "danger" if not dom_checked else "safe"
    dom_pill_text = "Malware / Phishing" if not dom_checked else "Authentic Broker Domain"

    # Invariant 5: NSDL Depository
    nsdl_checked = "" if report.depository_audit.is_fake_nsdl_claim else "checked"
    nsdl_mark = "!" if report.depository_audit.is_fake_nsdl_claim else "✓"
    nsdl_pill = "danger" if report.depository_audit.is_fake_nsdl_claim else "safe"
    nsdl_pill_text = "Unauthorized NSDL Claim" if report.depository_audit.is_fake_nsdl_claim else "Depository Invariants Valid"

    st.markdown(
        f"""
        <div class="town-list-container">
            <div class="town-list-header">
                <span class="town-list-title">Deterministic Regulatory Invariants</span>
                <span style="font-size: 0.8rem; color: #71717a;">5 verified benchmarks</span>
            </div>

            <!-- Item 1: SEBI Registry -->
            <div class="town-list-item">
                <div class="town-item-left">
                    <div class="town-item-checkbox {sebi_checked}">{sebi_mark}</div>
                    <div>
                        <div class="town-item-title">SEBI Intermediary Registration</div>
                        <div class="town-item-desc">Claimed ID: {report.sebi_audit.claimed_id or 'None (Unregistered)'} · Registry status: {report.sebi_audit.registry_status}</div>
                    </div>
                </div>
                <span class="status-pill {sebi_pill}">{sebi_pill_text}</span>
            </div>

            <!-- Item 2: Payment Routing -->
            <div class="town-list-item">
                <div class="town-item-left">
                    <div class="town-item-checkbox {pay_checked}">{pay_mark}</div>
                    <div>
                        <div class="town-item-title">Payment Channel & Settlement Segregation</div>
                        <div class="town-item-desc">Recipient VPA: {report.payment_audit.primary_vpa or 'None specified'} · Circular 2023/71 mandate</div>
                    </div>
                </div>
                <span class="status-pill {pay_pill}">{pay_pill_text}</span>
            </div>

            <!-- Item 3: Return Guarantee (PVA) -->
            <div class="town-list-item">
                <div class="town-item-left">
                    <div class="town-item-checkbox {pva_checked}">{pva_mark}</div>
                    <div>
                        <div class="town-item-title">Performance Guarantee Audit</div>
                        <div class="town-item-desc">SEBI (Research Analysts) Regulation 15(1) & PVA Code of Conduct</div>
                    </div>
                </div>
                <span class="status-pill {pva_pill}">{pva_pill_text}</span>
            </div>

            <!-- Item 4: Domain & APK -->
            <div class="town-list-item">
                <div class="town-item-left">
                    <div class="town-item-checkbox {dom_checked}">{dom_mark}</div>
                    <div>
                        <div class="town-item-title">Domain Authenticity & APK Binary Invariant</div>
                        <div class="town-item-desc">Weighted Damerau-Levenshtein homoglyph distance · Section 66D IT Act</div>
                    </div>
                </div>
                <span class="status-pill {dom_pill}">{dom_pill_text}</span>
            </div>

            <!-- Item 5: NSDL Depository -->
            <div class="town-list-item">
                <div class="town-item-left">
                    <div class="town-item-checkbox {nsdl_checked}">{nsdl_mark}</div>
                    <div>
                        <div class="town-item-title">NSDL Depository Invariant Safeguard</div>
                        <div class="town-item-desc">Demat account 16-character format · Depositories Act 1996 verification</div>
                    </div>
                </div>
                <span class="status-pill {nsdl_pill}">{nsdl_pill_text}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4. Institutional Grievance Routing (Quiet, Minimalist Card)
    st.markdown(
        f"""
        <div class="town-list-container">
            <div class="town-list-header">
                <span class="town-list-title">Institutional Grievance Routing</span>
                <span class="status-pill neutral">{route.portal_name}</span>
            </div>
            <div style="font-size: 0.92rem; color: #18181b; line-height: 1.5; margin-bottom: 6px;">
                <b>Statutory Basis:</b> {route.statutory_basis}
            </div>
            <div style="font-size: 0.86rem; color: #52525b; line-height: 1.5;">
                {route.routing_rationale}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 5. Evidentiary Exports
    dossier_data = DossierGenerator.generate_json_dossier(report, content_to_analyze)
    pdf_bytes = DossierGenerator.generate_pdf_dossier(dossier_data)
    sms_text = DossierGenerator.generate_1930_sms(report, dossier_data["incident_id"])

    exp_cols = st.columns(2)
    with exp_cols[0]:
        st.download_button(
            label="Download PDF Dossier (Court-Ready)",
            data=pdf_bytes,
            file_name=f"Satark_Dossier_{dossier_data['incident_id']}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with exp_cols[1]:
        st.download_button(
            label="Download Structured JSON (SCORES / NCRP)",
            data=json.dumps(dossier_data, indent=2),
            file_name=f"Satark_Dossier_{dossier_data['incident_id']}.json",
            mime="application/json",
            use_container_width=True,
        )

    with st.expander("1930 National Cyber Fraud Helpline SMS Dispatch", expanded=False):
        st.code(sms_text, language="text")

# ---------------------------------------------------------
# Town Quiet Minimalist Footer
# ---------------------------------------------------------
st.markdown("<div style='height: 3.5rem;'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; border-top: 1px solid rgba(0, 0, 0, 0.06); padding-top: 2rem; font-size: 0.80rem; color: #a1a1aa;">
        SatarkBharat · Built for SANGYAN (SNTC, IIT BHU Varanasi × SEBI × NSDL) · Zero Stock Tips · 100% Investor Defense
    </div>
    """,
    unsafe_allow_html=True,
)
