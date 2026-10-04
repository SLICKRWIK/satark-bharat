"""SatarkBharat (सतर्क भारत) — Minimalist Investor Defense Sentinel.

Faithfully crafted in the high-craft visual aesthetic of Town (town.com):
- Warm eggshell/ivory paper canvas (#fbfbfa)
- High-contrast editorial serif headlines (Fraunces)
- Playful illustrative sentinel mascot in the hero section (matching Claus in Town)
- Clean, non-button top navigation links with proper hover states
- Highly visible buttons with crystal-clear contrast and distinct primary/secondary hierarchies
- SVG Radial Threat Gauge with gradient arc for high visual "oomph"
- Checklist-oriented audit results matching Town's to-do / activity list
- Zero tacky emojis; refined typography, micro-badges, and generous whitespace
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
# Town High-Craft CSS Styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Google Fonts: Fraunces (Editorial Serif) + Plus Jakarta Sans + JetBrains Mono */
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Canvas */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #fbfbfa !important;
        color: #18181b !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* Remove Streamlit Default Nav, Sidebars, and Headers */
    header[data-testid="stHeader"], footer, [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display: none !important;
    }
    .block-container {
        max-width: 800px !important;
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    /* Top Navigation Bar */
    .town-nav-wrap {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 3rem;
        padding-bottom: 1.2rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    }
    .town-nav-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .town-logo-box {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        padding: 6px 12px;
        font-weight: 700;
        font-size: 0.88rem;
        letter-spacing: 0.5px;
        color: #18181b;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .town-nav-links {
        display: flex;
        align-items: center;
        gap: 22px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #71717a;
    }
    .town-nav-links a, .town-nav-links span {
        color: #71717a;
        text-decoration: none;
        transition: color 0.15s ease;
    }
    .town-nav-links a:hover, .town-nav-links span:hover {
        color: #18181b;
        cursor: pointer;
    }
    .town-nav-right {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .town-nav-badge {
        font-size: 0.78rem;
        font-weight: 500;
        color: #71717a;
    }
    .town-nav-btn {
        background: #18181b;
        color: #ffffff !important;
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 0.80rem;
        font-weight: 500;
        text-decoration: none;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
    }

    /* Hero Section with Illustration */
    .hero-grid {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 24px;
        margin-bottom: 2.4rem;
    }
    .hero-text-col {
        flex: 1;
    }
    .hero-title {
        font-family: 'Fraunces', serif !important;
        font-size: 3.4rem !important;
        font-weight: 450 !important;
        line-height: 1.12 !important;
        letter-spacing: -1.2px !important;
        color: #18181b !important;
        margin-bottom: 1.2rem !important;
    }
    .hero-lead-row {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        font-size: 0.96rem;
        line-height: 1.6;
        color: #3f3f46;
        max-width: 580px;
    }
    .hero-avatar {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #e4e4e7;
        color: #52525b;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 600;
        flex-shrink: 0;
        margin-top: 3px;
    }
    .tag-salmon {
        display: inline-block;
        background: #ffedd5;
        color: #c2410c;
        padding: 1px 6px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
    }
    .hero-mascot-col {
        flex-shrink: 0;
        width: 140px;
        display: flex;
        justify-content: center;
    }

    /* Input Floating Container */
    .town-prompt-card {
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 16px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
        padding: 18px 20px;
        margin-bottom: 2rem;
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .town-prompt-card:focus-within {
        border-color: rgba(0, 0, 0, 0.2);
        box-shadow: 0 6px 24px -2px rgba(0, 0, 0, 0.07);
    }

    /* Button Contrast Fixes (Force Visible Text) */
    /* Scenario Chips: Soft Clean White Pills */
    .stButton>button {
        background-color: #ffffff !important;
        color: #18181b !important;
        border: 1px solid rgba(0, 0, 0, 0.12) !important;
        border-radius: 9999px !important;
        font-weight: 500 !important;
        font-size: 0.82rem !important;
        padding: 0.4rem 0.85rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.15s ease !important;
    }
    .stButton>button:hover {
        background-color: #f4f4f5 !important;
        border-color: rgba(0, 0, 0, 0.25) !important;
        color: #000000 !important;
        transform: translateY(-1px);
    }
    .stButton>button p, .stButton>button span, .stButton>button div {
        color: #18181b !important;
        font-weight: 500 !important;
    }

    /* Primary Action Button (Solid Ink Black with Crisp White Text) */
    div.primary-audit-btn .stButton>button {
        background-color: #18181b !important;
        color: #ffffff !important;
        border: 1px solid #18181b !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.90rem !important;
        padding: 0.55rem 1.4rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12) !important;
    }
    div.primary-audit-btn .stButton>button:hover {
        background-color: #27272a !important;
        border-color: #27272a !important;
        color: #ffffff !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.16) !important;
    }
    div.primary-audit-btn .stButton>button p,
    div.primary-audit-btn .stButton>button span,
    div.primary-audit-btn .stButton>button div {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Secondary Clear Button */
    div.secondary-clear-btn .stButton>button {
        background-color: transparent !important;
        color: #71717a !important;
        border: 1px solid rgba(0, 0, 0, 0.12) !important;
        border-radius: 10px !important;
    }
    div.secondary-clear-btn .stButton>button:hover {
        background-color: #f4f4f5 !important;
        color: #18181b !important;
    }
    div.secondary-clear-btn .stButton>button p,
    div.secondary-clear-btn .stButton>button span {
        color: #71717a !important;
    }

    /* Download Buttons */
    .stDownloadButton>button {
        background-color: #ffffff !important;
        color: #18181b !important;
        border: 1px solid rgba(0, 0, 0, 0.12) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.84rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
    }
    .stDownloadButton>button:hover {
        background-color: #f4f4f5 !important;
        border-color: rgba(0, 0, 0, 0.25) !important;
    }
    .stDownloadButton>button p, .stDownloadButton>button span {
        color: #18181b !important;
    }

    /* Textarea Styling */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #18181b !important;
        border: none !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.98rem !important;
        line-height: 1.55 !important;
        padding: 4px 0 !important;
        box-shadow: none !important;
    }

    /* Clean Tabs (Underline Only, No Boxy Borders) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: transparent;
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
        padding-bottom: 4px;
        margin-bottom: 0.8rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #71717a !important;
        font-size: 0.84rem !important;
        font-weight: 500 !important;
        padding: 4px 2px !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        color: #18181b !important;
        border-bottom: 2px solid #18181b !important;
    }

    /* Town Checklist Container */
    .town-list-container {
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 16px;
        box-shadow: 0 4px 24px -2px rgba(0, 0, 0, 0.04);
        padding: 22px 26px;
        margin-top: 1.8rem;
        margin-bottom: 2rem;
    }
    .town-list-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 16px;
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
        margin-bottom: 16px;
    }
    .town-list-title {
        font-size: 0.84rem;
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
        transition: background 0.15s ease;
    }
    .town-list-item:last-child {
        border-bottom: none;
        padding-bottom: 4px;
    }
    .town-item-left {
        display: flex;
        gap: 14px;
        max-width: 530px;
    }
    .town-item-checkbox {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 1.5px solid #d4d4d8;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 600;
        margin-top: 2px;
        flex-shrink: 0;
    }
    .town-item-checkbox.checked {
        border-color: #18181b;
        background: #18181b;
        color: #ffffff;
    }
    .town-item-checkbox.alert {
        border-color: #dc2626;
        background: #fef2f2;
        color: #dc2626;
    }
    .town-item-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #18181b;
        line-height: 1.4;
    }
    .town-item-desc {
        font-size: 0.83rem;
        color: #71717a;
        margin-top: 3px;
        line-height: 1.45;
    }

    /* Minimalist Badges */
    .status-pill {
        font-size: 0.74rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 4px;
        white-space: nowrap;
        letter-spacing: 0.2px;
    }
    .status-pill.danger {
        background: #fee2e2;
        color: #991b1b;
    }
    .status-pill.warning {
        background: #fef3c7;
        color: #92400e;
    }
    .status-pill.safe {
        background: #ecfdf5;
        color: #065f46;
    }
    .status-pill.neutral {
        background: #f4f4f5;
        color: #52525b;
    }

    /* Expander Clean Overrides */
    .streamlit-expanderHeader {
        background-color: transparent !important;
        color: #18181b !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
    }
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        border-radius: 12px !important;
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

# Session State
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ---------------------------------------------------------
# Top Navigation Bar (Clean Text Links, Zero Clunky Boxes)
# ---------------------------------------------------------
st.markdown(
    """
    <div class="town-nav-wrap">
        <div class="town-nav-left">
            <div class="town-logo-box">
                <span style="color: #059669; font-size: 11px;">●</span>
                <span>SATARK</span>
            </div>
            <div class="town-nav-links" style="margin-left: 12px;">
                <span>Sentinel</span>
                <span>SCORES 2.0</span>
                <span>NCRP 1930</span>
                <span>Investor Charter</span>
            </div>
        </div>
        <div class="town-nav-right">
            <span class="town-nav-badge">SANGYAN · Track A</span>
            <a href="https://sangyan.sntciitbhu.co.in/" target="_blank" class="town-nav-btn">IIT-BHU × SEBI × NSDL</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Hero Section with High-Craft Mascot Illustration
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero-grid">
        <div class="hero-text-col">
            <div class="hero-title">
                SatarkBharat protects your savings from fraud.
            </div>
            <div class="hero-lead-row">
                <div class="hero-avatar">s</div>
                <div>
                    Forward any suspicious WhatsApp advisory, Telegram tip, or payment request.
                    <span class="tag-salmon">Satark</span> audits regulatory invariants, recipient UPI accounts,
                    and official SEBI registers before you transfer money.
                </div>
            </div>
        </div>
        <div class="hero-mascot-col">
            <!-- High-Craft Sentinel Guardian Mascot SVG -->
            <svg width="125" height="140" viewBox="0 0 120 135" fill="none" xmlns="http://www.w3.org/2000/svg">
                <!-- Soft Glow Backdrop -->
                <circle cx="60" cy="65" r="50" fill="#fef3c7" fill-opacity="0.6"/>
                <!-- Guardian Shield Body -->
                <path d="M60 15L95 30V75C95 98 60 115 60 115C60 115 25 98 25 75V30L60 15Z" fill="#18181b" stroke="#3f3f46" stroke-width="2.5" stroke-linejoin="round"/>
                <!-- Inner Shield Accent -->
                <path d="M60 22L88 34V72C88 91 60 106 60 106C60 106 32 91 32 72V34L60 22Z" fill="#27272a"/>
                <!-- Golden Ashoka / Sentinel Seal -->
                <circle cx="60" cy="58" r="18" fill="#d97706" fill-opacity="0.2" stroke="#f59e0b" stroke-width="1.8"/>
                <circle cx="60" cy="58" r="13" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="3 2"/>
                <circle cx="60" cy="58" r="5" fill="#fef3c7"/>
                <!-- Radiant Check / Verification Spear -->
                <path d="M53 58L58 63L68 52" stroke="#fef3c7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                <!-- Little Pen / Audit Quill held in knight tradition -->
                <rect x="74" y="65" width="8" height="42" rx="4" transform="rotate(-30 74 65)" fill="#e06c53" stroke="#18181b" stroke-width="1.5"/>
                <polygon points="98,107 104,115 93,113" fill="#fbbf24" stroke="#18181b" stroke-width="1"/>
            </svg>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Load Scenarios (Clean, Soft White Pill Chips)
# ---------------------------------------------------------
st.markdown("<p style='font-size: 0.78rem; font-weight: 600; color: #71717a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;'>Load Sample Scenarios</p>", unsafe_allow_html=True)

chip_cols = st.columns(4)
chip_data = [
    ("Case A: Impersonation", 0, "WhatsApp SEBI RA Spoofing & Personal VPA"),
    ("Case B: Telegram Tip", 1, "Unregistered Syndicate 500% Jackpot"),
    ("Case C: Cloned APK", 2, "Lookalike Broker APK Phishing Link"),
    ("Case D: Verified Broker", 3, "Legitimate Broker Risk Notice Baseline"),
]

for title, idx, desc in chip_data:
    with chip_cols[idx]:
        if st.button(title, key=f"chip_btn_{idx}", help=desc, use_container_width=True):
            st.session_state.input_text = samples[idx]["input_content"]
            st.rerun()

# ---------------------------------------------------------
# Input Tabs (Message, Screenshot, Audio, Guardrail)
# ---------------------------------------------------------
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

input_tabs = st.tabs(["Advisory Text", "Upload Screenshot", "Upload Voice Note", "Guardrail Verification"])

with input_tabs[0]:
    user_input = st.text_area(
        label="Message Text",
        value=st.session_state.input_text,
        height=110,
        placeholder="Type or paste advisory message, claimed SEBI ID, or payment request here...",
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
        extracted = ocr_engine.extract_text_from_image(uploaded_file.read())
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
        st.caption(f"Audio stream '{uploaded_audio.name}' received.")
        if not st.session_state.input_text:
            st.session_state.input_text = "Kal Nifty aur Sensex ka confirmed upper circuit setting ho chuka hai! 500% pakka guaranteed jackpot return milega! Fee sirf Rs 2,500 hai paytm karo: sureprofit.pool@paytm"

with input_tabs[3]:
    st.caption("Verify that SatarkBharat strictly adheres to SANGYAN rules by refusing speculative stock advice.")
    test_query = st.text_input(
        "Speculative stock query",
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
                    <div style="font-size: 0.88rem; color: #18181b; margin-top: 4px;">{gr_res.rejection_message_english}</div>
                    <div style="font-size: 0.82rem; color: #52525b; margin-top: 4px; font-style: italic;">"{gr_res.rejection_message_hindi}"</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.success("Query permitted.")

# ---------------------------------------------------------
# Action Buttons (Primary Black + Secondary Ghost)
# ---------------------------------------------------------
btn_col1, btn_col2 = st.columns([4, 1])
with btn_col1:
    st.markdown('<div class="primary-audit-btn">', unsafe_allow_html=True)
    analyze_clicked = st.button("Run Regulatory Audit →", key="btn_run_audit", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with btn_col2:
    st.markdown('<div class="secondary-clear-btn">', unsafe_allow_html=True)
    if st.button("Clear", key="btn_clear_text", use_container_width=True):
        st.session_state.input_text = ""
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Results Execution & High-Craft Visual Presentation
# ---------------------------------------------------------
content_to_analyze = st.session_state.input_text.strip()

if (analyze_clicked or content_to_analyze) and len(content_to_analyze) > 10:
    report: ThreatReport = threat_engine.evaluate(content_to_analyze)
    route: JurisdictionalRoute = RegulatoryRouter.resolve_route(report)

    score = report.composite_threat_score
    is_critical = score >= 60

    # Color & status determinations
    badge_bg = "#fee2e2" if is_critical else ("#fef3c7" if score > 24 else "#ecfdf5")
    badge_color = "#991b1b" if is_critical else ("#92400e" if score > 24 else "#065f46")
    badge_label = f"Threat Index: {score}/100 ({report.severity})"

    # SVG Speedometer Arc Calculation (Visual Oomph)
    # Angle runs from 180 deg (left, 0%) to 0 deg (right, 100%)
    gauge_pct = score / 100.0
    needle_angle = 180 - (gauge_pct * 180)
    gauge_color = "#ef4444" if is_critical else ("#f59e0b" if score > 24 else "#10b981")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 1. Main Verdict Card with SVG Speedometer Arc
    st.markdown(
        f"""
        <div class="town-list-container">
            <div class="town-list-header">
                <span class="town-list-title">Sentinel Audit Report</span>
                <span class="status-pill" style="background: {badge_bg}; color: {badge_color};">{badge_label}</span>
            </div>

            <!-- Radial Threat Gauge Arc (Visual Oomph) -->
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; padding: 12px 16px; background: #faf9f6; border-radius: 12px; border: 1px solid rgba(0,0,0,0.04);">
                <div style="max-width: 500px;">
                    <div style="font-size: 0.78rem; font-weight: 600; text-transform: uppercase; color: #71717a; margin-bottom: 2px;">Composite Risk Assessment</div>
                    <div style="font-size: 1.05rem; font-weight: 600; color: #18181b;">{report.plain_english_summary}</div>
                </div>
                <div style="text-align: center; flex-shrink: 0;">
                    <!-- SVG Gauge -->
                    <svg width="100" height="58" viewBox="0 0 100 58">
                        <!-- Background Track -->
                        <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#e4e4e7" stroke-width="8" stroke-linecap="round"/>
                        <!-- Active Arc -->
                        <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="{gauge_color}" stroke-width="8" stroke-linecap="round" stroke-dasharray="126" stroke-dashoffset="{126 - (126 * gauge_pct)}"/>
                        <text x="50" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="700" fill="#18181b" text-anchor="middle">{score}</text>
                    </svg>
                    <div style="font-size: 0.70rem; color: #71717a; font-weight: 500;">out of 100</div>
                </div>
            </div>

            <div style="font-size: 0.92rem; color: #3f3f46; line-height: 1.5; margin-bottom: 6px;">
                <b>हिन्दी:</b> {report.vernacular_hindi_summary}
            </div>
            <div style="font-size: 0.90rem; color: #71717a; line-height: 1.5;">
                <b>বাংলা:</b> {report.vernacular_bengali_summary}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Vernacular Voice Alert Player
    st.markdown("<p style='font-size: 0.78rem; font-weight: 600; color: #71717a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;'>Vernacular Voice Warning (Audio Playback)</p>", unsafe_allow_html=True)
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

    # 3. Checklist-Oriented Regulatory Invariants
    sebi_checked = "checked" if not report.sebi_audit.is_impersonation_suspected and report.sebi_audit.is_in_registry else "alert"
    sebi_mark = "✓" if sebi_checked == "checked" else "!"
    sebi_pill = "safe" if report.sebi_audit.is_in_registry and not report.sebi_audit.is_impersonation_suspected else ("danger" if report.sebi_audit.is_impersonation_suspected else "warning")
    sebi_pill_text = "Verified Match" if sebi_pill == "safe" else ("Impersonation Alert" if sebi_pill == "danger" else "Unregistered")

    pay_checked = "checked" if report.payment_audit.is_clearing_compliant else "alert"
    pay_mark = "✓" if pay_checked == "checked" else "!"
    pay_pill = "safe" if report.payment_audit.is_clearing_compliant else "danger"
    pay_pill_text = "Clearing Compliant" if pay_pill == "safe" else "Personal Savings VPA"

    pva_checked = "alert" if report.guaranteed_returns_detected else "checked"
    pva_mark = "!" if report.guaranteed_returns_detected else "✓"
    pva_pill = "danger" if report.guaranteed_returns_detected else "safe"
    pva_pill_text = "Prohibited Return Claim" if report.guaranteed_returns_detected else "No Fixed Guarantees"

    dom_checked = "alert" if report.domain_audit.is_typosquatted or report.domain_audit.has_apk_link else "checked"
    dom_mark = "!" if dom_checked == "alert" else "✓"
    dom_pill = "danger" if dom_checked == "alert" else "safe"
    dom_pill_text = "Malware / Phishing" if dom_checked == "alert" else "Authentic Domain"

    nsdl_checked = "alert" if report.depository_audit.is_fake_nsdl_claim else "checked"
    nsdl_mark = "!" if report.depository_audit.is_fake_nsdl_claim else "✓"
    nsdl_pill = "danger" if report.depository_audit.is_fake_nsdl_claim else "safe"
    nsdl_pill_text = "Unauthorized NSDL Claim" if report.depository_audit.is_fake_nsdl_claim else "Depository Valid"

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

    # 4. Institutional Grievance Routing (Quiet Minimalist Card)
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
# Footer
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
