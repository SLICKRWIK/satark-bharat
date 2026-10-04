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

import base64
import importlib
import json
import textwrap

import streamlit as st

import satark_bharat.decision.threat_engine
import satark_bharat.ingestion.audio
import satark_bharat.ingestion.ocr
import satark_bharat.redressal.dossier

importlib.reload(satark_bharat.ingestion.ocr)
importlib.reload(satark_bharat.ingestion.audio)
importlib.reload(satark_bharat.redressal.dossier)
importlib.reload(satark_bharat.decision.threat_engine)

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
        padding-top: 4rem !important;
        padding-bottom: 5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    /* Continuous Professional Financial/Regulatory Ticker Bar at Top */
    .top-ticker-bar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 36px;
        background: #09090b;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        overflow: hidden;
        z-index: 999999;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.35);
    }
    .ticker-track {
        display: flex;
        align-items: center;
        white-space: nowrap;
        will-change: transform;
        animation: ticker-scroll 38s linear infinite;
    }
    .top-ticker-bar:hover .ticker-track {
        animation-play-state: paused;
    }
    @keyframes ticker-scroll {
        0% {
            transform: translate3d(0, 0, 0);
        }
        100% {
            transform: translate3d(-50%, 0, 0);
        }
    }
    .ticker-item {
        display: inline-flex;
        align-items: center;
        padding: 0 16px;
    }
    .ticker-lbl {
        color: #e4e4e7;
        font-weight: 500;
        margin-right: 6px;
    }
    .ticker-val {
        color: #fbbf24;
        font-weight: 600;
    }

    .ticker-sep {
        color: rgba(255, 255, 255, 0.22);
        margin-left: 16px;
        font-weight: 300;
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

    /* ---------------------------------------------------------
       Distinct, Refined Button Palettes & Micro-Animations
       --------------------------------------------------------- */
    /* Global Base Reset for Streamlit Buttons */
    div[data-testid="stButton"] button,
    button[kind="secondary"],
    button[kind="primary"],
    [data-testid="stBaseButton-secondary"],
    [data-testid="stBaseButton-primary"],
    [data-testid="baseButton-secondary"],
    [data-testid="baseButton-primary"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        outline: none !important;
    }

    /* 1. SCENARIO PILLS (Case A, B, C, D): Soft White Pills with Dark Charcoal Text */
    div[class*="st-key-chip_btn_"] button,
    div[data-testid="stButton"] button[key*="chip_btn_"] {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #27272a !important;
        border: 1px solid rgba(0, 0, 0, 0.12) !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        letter-spacing: -0.05px !important;
        padding: 0.45rem 0.85rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
    }

    div[class*="st-key-chip_btn_"] button *,
    div[class*="st-key-chip_btn_"] button p,
    div[class*="st-key-chip_btn_"] button span {
        color: #27272a !important;
        -webkit-text-fill-color: #27272a !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        transition: color 0.15s ease !important;
    }

    div[class*="st-key-chip_btn_"] button:hover {
        background-color: #fbfbfa !important;
        background: #fbfbfa !important;
        border-color: #18181b !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.07) !important;
    }

    div[class*="st-key-chip_btn_"] button:hover *,
    div[class*="st-key-chip_btn_"] button:hover p,
    div[class*="st-key-chip_btn_"] button:hover span {
        color: #09090b !important;
        -webkit-text-fill-color: #09090b !important;
    }

    div[class*="st-key-chip_btn_"] button:active {
        transform: translateY(0) scale(0.98) !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
    }

    /* 2. PRIMARY AUDIT BUTTON: Ink Obsidian with Distinct Lift & Subtle Glow */
    div.st-key-btn_run_audit button,
    button[kind="primary"],
    [data-testid="stBaseButton-primary"],
    [data-testid="baseButton-primary"] {
        background-color: #18181b !important;
        background: linear-gradient(180deg, #27272a 0%, #18181b 100%) !important;
        color: #ffffff !important;
        border: 1px solid #18181b !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        letter-spacing: 0.25px !important;
        padding: 0.65rem 1.4rem !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.12), 0 6px 14px -3px rgba(0, 0, 0, 0.1) !important;
    }

    div.st-key-btn_run_audit button *,
    div.st-key-btn_run_audit button p,
    div.st-key-btn_run_audit button span,
    button[kind="primary"] *,
    button[kind="primary"] p,
    button[kind="primary"] span,
    [data-testid="stBaseButton-primary"] *,
    [data-testid="baseButton-primary"] * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        letter-spacing: 0.25px !important;
    }

    div.st-key-btn_run_audit button:hover,
    button[kind="primary"]:hover,
    [data-testid="stBaseButton-primary"]:hover,
    [data-testid="baseButton-primary"]:hover {
        background-color: #09090b !important;
        background: #09090b !important;
        border-color: #000000 !important;
        transform: translateY(-2px) scale(1.005) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2), 0 12px 24px -4px rgba(0, 0, 0, 0.14) !important;
    }

    div.st-key-btn_run_audit button:active,
    button[kind="primary"]:active,
    [data-testid="stBaseButton-primary"]:active,
    [data-testid="baseButton-primary"]:active {
        transform: translateY(0) scale(0.99) !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12) !important;
    }

    /* 3. SECONDARY CLEAR BUTTON: Ghost / Soft Neutral Outline */
    div.st-key-btn_clear_text button {
        background-color: #f4f4f5 !important;
        background: #f4f4f5 !important;
        color: #71717a !important;
        border: 1px solid #e4e4e7 !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 0.65rem 1rem !important;
        box-shadow: none !important;
    }

    div.st-key-btn_clear_text button *,
    div.st-key-btn_clear_text button p,
    div.st-key-btn_clear_text button span {
        color: #71717a !important;
        -webkit-text-fill-color: #71717a !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        transition: color 0.15s ease !important;
    }

    div.st-key-btn_clear_text button:hover {
        background-color: #ffffff !important;
        background: #ffffff !important;
        border-color: #d4d4d8 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }

    div.st-key-btn_clear_text button:hover *,
    div.st-key-btn_clear_text button:hover p,
    div.st-key-btn_clear_text button:hover span {
        color: #18181b !important;
        -webkit-text-fill-color: #18181b !important;
    }

    div.st-key-btn_clear_text button:active {
        transform: translateY(0) scale(0.98) !important;
    }

    /* 4. OTHER BUTTONS: Downloads & Guardrail Test */
    div.st-key-btn_test_guardrail button,
    .stDownloadButton button,
    div[data-testid="stDownloadButton"] button {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #18181b !important;
        border: 1px solid rgba(0, 0, 0, 0.12) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.86rem !important;
        padding: 0.65rem 1rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    div.st-key-btn_test_guardrail button *,
    div.st-key-btn_test_guardrail button p,
    div.st-key-btn_test_guardrail button span,
    .stDownloadButton button *,
    .stDownloadButton button p,
    .stDownloadButton button span,
    div[data-testid="stDownloadButton"] button * {
        color: #18181b !important;
        -webkit-text-fill-color: #18181b !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.86rem !important;
    }

    div.st-key-btn_test_guardrail button:hover,
    .stDownloadButton button:hover,
    div[data-testid="stDownloadButton"] button:hover {
        background-color: #faf9f6 !important;
        border-color: #18181b !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08) !important;
    }

    /* Minimal Language Switcher in Card Header */
    .lang-switcher {
        display: inline-flex;
        align-items: center;
        background: #f4f4f5;
        border-radius: 6px;
        padding: 2px;
        border: 1px solid rgba(0, 0, 0, 0.06);
        gap: 2px;
        margin-left: 6px;
    }
    .lang-tab {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 4px !important;
        font-size: 0.72rem !important;
        font-weight: 500 !important;
        color: #71717a !important;
        -webkit-text-fill-color: #71717a !important;
        padding: 2px 7px !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        line-height: 1.2 !important;
        box-shadow: none !important;
    }
    .lang-tab:hover {
        color: #18181b !important;
        -webkit-text-fill-color: #18181b !important;
    }
    .lang-tab.active {
        background: #ffffff !important;
        background-color: #ffffff !important;
        color: #18181b !important;
        -webkit-text-fill-color: #18181b !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08) !important;
    }

    /* Standalone Minimalist Speaker Icon (No Border Box, Realistic Vector) */
    .speaker-icon-btn {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        width: 24px !important;
        height: 24px !important;
        padding: 0 !important;
        margin: 0 !important;
        cursor: pointer !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        outline: none !important;
        transition: transform 0.15s ease, opacity 0.15s ease !important;
    }
    .speaker-icon {
        width: 20px;
        height: 20px;
        background-color: #9ca3af;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolygon points='11 5 6 9 2 9 2 15 6 15 11 19 11 5' fill='black'/%3E%3Cpath d='M15.54 8.46a5 5 0 0 1 0 7.07'/%3E%3Cpath d='M19.07 4.93a10 10 0 0 1 0 14.14'/%3E%3C/svg%3E") no-repeat center / contain;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolygon points='11 5 6 9 2 9 2 15 6 15 11 19 11 5' fill='black'/%3E%3Cpath d='M15.54 8.46a5 5 0 0 1 0 7.07'/%3E%3Cpath d='M19.07 4.93a10 10 0 0 1 0 14.14'/%3E%3C/svg%3E") no-repeat center / contain;
        transition: background-color 0.15s ease, transform 0.15s ease;
    }
    .speaker-icon-btn:hover .speaker-icon {
        background-color: #18181b !important;
        transform: scale(1.08) !important;
    }
    .speaker-icon-btn.speaking .speaker-icon {
        background-color: #18181b !important;
        animation: speaker-blink 0.75s ease-in-out infinite !important;
    }
    @keyframes speaker-blink {
        0%, 100% {
            opacity: 1;
            transform: scale(1.12);
        }
        50% {
            opacity: 0.2;
            transform: scale(0.9);
        }
    }

    /* Textarea Styling & Generous Inset Padding */
    div[data-testid="stTextArea"] {
        margin-top: 6px;
    }
    div[data-baseweb="textarea"] {
        border-radius: 12px !important;
        border: 1px solid rgba(0, 0, 0, 0.12) !important;
        background-color: #ffffff !important;
        padding: 4px 6px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }
    div[data-baseweb="textarea"]:focus-within {
        border-color: #18181b !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08) !important;
    }
    .stTextArea textarea {
        background-color: transparent !important;
        color: #18181b !important;
        border: none !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        padding: 12px 14px !important;
        box-shadow: none !important;
    }
    .stTextArea textarea::placeholder {
        color: #a1a1aa !important;
        font-size: 0.90rem !important;
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
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        font-size: 0.84rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: #71717a;
    }
    .town-list-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 13px 0;
        border-bottom: 1px solid rgba(0, 0, 0, 0.04);
        transition: background 0.15s ease;
    }
    .town-list-item:last-child {
        border-bottom: none;
        padding-bottom: 4px;
    }
    .town-item-content {
        max-width: 540px;
    }
    .town-item-title {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        font-size: 0.94rem;
        font-weight: 600;
        color: #18181b;
        line-height: 1.4;
        letter-spacing: -0.15px;
    }
    .town-item-desc {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        font-size: 0.82rem;
        color: #71717a;
        margin-top: 3px;
        line-height: 1.45;
        letter-spacing: 0.05px;
    }

    /* Pure Typographic Invariant Status (No Pill / No Box / Elegant Color Only) */
    .invariant-status {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px !important;
        white-space: nowrap !important;
        text-align: right !important;
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    .invariant-status.warning {
        color: #d97706 !important;
    }
    .invariant-status.danger {
        color: #dc2626 !important;
    }
    .invariant-status.safe {
        color: #059669 !important;
    }
    .invariant-status.neutral {
        color: #71717a !important;
    }

    /* Minimalist Badges for Institutional Grievance Routing */
    .status-pill {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
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

    /* Clean 1930 SMS Dispatch Box */
    .sms-dispatch-details {
        margin-top: 14px;
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 12px;
        overflow: hidden;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .sms-dispatch-details:hover {
        border-color: rgba(0, 0, 0, 0.18);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    .sms-dispatch-summary {
        padding: 12px 16px;
        background-color: #faf9f6;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: space-between;
        user-select: none;
        list-style: none;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .sms-dispatch-summary::-webkit-details-marker,
    .sms-dispatch-summary::marker {
        display: none !important;
    }
    .sms-dispatch-body {
        padding: 14px 16px;
        background: #ffffff;
        border-top: 1px solid rgba(0, 0, 0, 0.05);
    }
    .sms-dispatch-pre {
        margin: 0;
        padding: 12px 14px;
        background: #faf9f6;
        border: 1px solid rgba(0, 0, 0, 0.06);
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.81rem;
        line-height: 1.55;
        color: #18181b;
        white-space: pre-wrap;
        word-break: break-all;
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
    )

threat_engine, guardrail, voice_engine = get_engines()
ocr_engine = VisualOcrIngestion()

# Load Sample Scenarios
@st.cache_data
def load_sample_scenarios():
    if SAMPLES_PATH.exists():
        with open(SAMPLES_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []

samples = load_sample_scenarios()

# Session State
if "manual_input" not in st.session_state:
    st.session_state.manual_input = ""
if "screenshot_input" not in st.session_state:
    st.session_state.screenshot_input = ""
if "audio_input" not in st.session_state:
    st.session_state.audio_input = ""
if "sample_input" not in st.session_state:
    st.session_state.sample_input = ""
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "manual"
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "audit_executed" not in st.session_state:
    st.session_state.audit_executed = False

# ---------------------------------------------------------
# Top Scrolling Regulatory Ticker Tape (Black Institutional Bar)
# ---------------------------------------------------------
ticker_items = """
    <span class="ticker-item"><span class="ticker-lbl">SATARK</span><span class="ticker-val">SENTINEL ACTIVE</span><span class="ticker-sep">|</span></span>
    <span class="ticker-item"><span class="ticker-lbl">SANGYAN 2024</span><span class="ticker-val">SNTC IIT-BHU × SEBI × NSDL</span><span class="ticker-sep">|</span></span>
    <span class="ticker-item"><span class="ticker-lbl">TRACK.A</span><span class="ticker-val">FRAUD RESILIENCE BENCHMARK</span><span class="ticker-sep">|</span></span>
    <span class="ticker-item"><span class="ticker-lbl">SEBI MANDATE</span><span class="ticker-val">CIRCULAR 2023/71 POOLING PROHIBITED</span><span class="ticker-sep">|</span></span>
    <span class="ticker-item"><span class="ticker-lbl">RA REG 15(1)</span><span class="ticker-val">GUARANTEED RETURNS BANNED</span><span class="ticker-sep">|</span></span>
    <span class="ticker-item"><span class="ticker-lbl">NCRP HELPLINE</span><span class="ticker-val">DIAL 1930 FOR CYBER FINANCIAL FRAUD</span><span class="ticker-sep">|</span></span>
    <span class="ticker-item"><span class="ticker-lbl">INSTITUTIONAL REDRESSAL</span><span class="ticker-val">SCORES 2.0 & SMART ODR PORTAL</span><span class="ticker-sep">|</span></span>
    <span class="ticker-item"><span class="ticker-lbl">NSDL INVARIANT</span><span class="ticker-val">16-DIGIT DEMAT VERIFICATION</span><span class="ticker-sep">|</span></span>
    <span class="ticker-item"><span class="ticker-lbl">SENTINEL INTEGRITY</span><span class="ticker-val">ZERO STOCK SPECULATION / 100% DEFENSE</span><span class="ticker-sep">|</span></span>
"""

st.html(
    textwrap.dedent(
        f"""
        <div class="top-ticker-bar">
            <div class="ticker-track">
                {ticker_items}
                {ticker_items}
            </div>
        </div>
        """
    )
)

# ---------------------------------------------------------
# Hero Section with High-Craft Mascot Illustration
# ---------------------------------------------------------
st.html(
    textwrap.dedent(
        """
        <div class="hero-grid">
            <div class="hero-text-col">
                <div class="hero-title">
                    SatarkBharat protects your savings from fraud.
                </div>
                <div class="hero-lead-row">
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
        """
    )
)

# ---------------------------------------------------------
# Load Scenarios (Clean, Soft White Pill Chips)
# ---------------------------------------------------------
st.html("<p style='font-size: 0.78rem; font-weight: 600; color: #71717a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;'>Load Sample Scenarios</p>")

chip_cols = st.columns(4)
chip_data = [
    ("Case A: Impersonation", 0, "WhatsApp SEBI RA Spoofing & Personal VPA"),
    ("Case B: Telegram Tip", 1, "Unregistered Syndicate 500% Jackpot"),
    ("Case C: Cloned APK", 2, "Lookalike Broker APK Phishing Link"),
    ("Case D: Verified Broker", 3, "Legitimate Broker Risk Notice Baseline"),
]

for title, idx, _ in chip_data:
    with chip_cols[idx]:
        if st.button(title, key=f"chip_btn_{idx}", use_container_width=True):
            content = samples[idx]["input_content"]
            st.session_state.sample_input = content
            st.session_state.manual_input = content
            st.session_state.active_tab = "sample"
            st.session_state.audit_executed = False
            st.rerun()

# ---------------------------------------------------------
# Input Tabs (Message, Screenshot, Audio, Guardrail)
# ---------------------------------------------------------
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

input_tabs = st.tabs(["Advisory Text", "Upload Screenshot", "Upload Voice Note"])

with input_tabs[0]:
    user_text = st.text_area(
        label="Message Text",
        value=st.session_state.manual_input,
        height=110,
        placeholder="Type or paste advisory message, claimed SEBI ID, or payment request here...",
        label_visibility="collapsed",
    )
    if user_text != st.session_state.manual_input:
        st.session_state.manual_input = user_text
        st.session_state.active_tab = "manual"
        st.session_state.audit_executed = False

with input_tabs[1]:
    uploaded_file = st.file_uploader(
        "Upload Screenshot",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed",
        key="screenshot_uploader_file",
    )
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        file_hash = f"{uploaded_file.name}_{len(file_bytes)}"
        if st.session_state.get("last_uploaded_screenshot_hash") != file_hash:
            st.session_state.last_uploaded_screenshot_hash = file_hash
            with st.spinner("Extracting advisory tokens with Gemini Multimodal Vision Sentinel..."):
                try:
                    extracted = ocr_engine.extract_text_from_image(file_bytes, mime_type=uploaded_file.type or "image/png")
                except TypeError:
                    extracted = ocr_engine.extract_text_from_image(file_bytes)
                st.session_state.screenshot_input = extracted
                st.session_state.active_tab = "screenshot"
                st.session_state.audit_executed = False
                st.rerun()

        col_img, col_txt = st.columns([1, 2], gap="medium")
        with col_img:
            st.image(uploaded_file, caption="Evidence Screenshot")
        with col_txt:
            st.markdown(
                """
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                    <span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #52525b;">Extracted Advisory Transcription</span>
                    <span style="font-size: 0.70rem; font-weight: 600; color: #71717a; background: #f4f4f5; padding: 2px 8px; border-radius: 9999px; border: 1px solid #e4e4e7;">Gemini Multimodal Vision</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            sc_text = st.text_area(
                "Extracted Text Review",
                value=st.session_state.screenshot_input,
                height=280,
                label_visibility="collapsed",
            )
            st.markdown("<div style='font-size: 0.72rem; color: #a1a1aa; margin-top: 4px;'>Review, edit, or append details prior to regulatory compliance audit.</div>", unsafe_allow_html=True)
            if sc_text != st.session_state.screenshot_input:
                st.session_state.screenshot_input = sc_text
                st.session_state.active_tab = "screenshot"
                st.session_state.audit_executed = False

with input_tabs[2]:
    uploaded_audio = st.file_uploader(
        "Upload Voice Note",
        type=["mp3", "wav", "ogg", "m4a"],
        label_visibility="collapsed",
        key="audio_uploader_file",
    )
    if uploaded_audio is not None:
        audio_bytes = uploaded_audio.getvalue()
        audio_hash = f"{uploaded_audio.name}_{len(audio_bytes)}"
        if st.session_state.get("last_uploaded_audio_hash") != audio_hash:
            st.session_state.last_uploaded_audio_hash = audio_hash
            with st.spinner("Transcribing vernacular speech with Gemini Speech Sentinel..."):
                transcribed = voice_engine.transcribe_audio(audio_bytes, filename=uploaded_audio.name)
                st.session_state.audio_input = transcribed
                st.session_state.active_tab = "audio"
                st.session_state.audit_executed = False
                st.rerun()

        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: space-between; margin: 8px 0;">
                <span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #52525b;">Speech Transcription</span>
                <span style="font-size: 0.70rem; font-weight: 600; color: #71717a; background: #f4f4f5; padding: 2px 8px; border-radius: 9999px; border: 1px solid #e4e4e7;">Gemini Speech Sentinel</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        audio_text = st.text_area(
            "Transcribed Audio Text Review",
            value=st.session_state.audio_input,
            height=140,
            label_visibility="collapsed",
        )
        st.markdown("<div style='font-size: 0.72rem; color: #a1a1aa; margin-top: 4px;'>Regional speech transcribed verbatim into advisory buffer.</div>", unsafe_allow_html=True)
        if audio_text != st.session_state.audio_input:
            st.session_state.audio_input = audio_text
            st.session_state.active_tab = "audio"
            st.session_state.audit_executed = False

# ---------------------------------------------------------
# ---------------------------------------------------------
# Action Buttons (Primary Black + Secondary Ghost)
# ---------------------------------------------------------
btn_col1, btn_col2 = st.columns([4, 1])
with btn_col1:
    analyze_clicked = st.button("Run Regulatory Audit →", key="btn_run_audit", type="primary", use_container_width=True)
    if analyze_clicked:
        st.session_state.audit_executed = True

with btn_col2:
    if st.button("Clear", key="btn_clear_text", use_container_width=True):
        st.session_state.manual_input = ""
        st.session_state.screenshot_input = ""
        st.session_state.audio_input = ""
        st.session_state.sample_input = ""
        st.session_state.input_text = ""
        st.session_state.active_tab = "manual"
        st.session_state.audit_executed = False
        if "last_uploaded_screenshot_hash" in st.session_state:
            del st.session_state["last_uploaded_screenshot_hash"]
        if "last_uploaded_audio_hash" in st.session_state:
            del st.session_state["last_uploaded_audio_hash"]
        st.rerun()

# ---------------------------------------------------------
# Results Execution & High-Craft Visual Presentation
# ---------------------------------------------------------
if st.session_state.active_tab == "screenshot" and st.session_state.screenshot_input.strip():
    content_to_analyze = st.session_state.screenshot_input.strip()
elif st.session_state.active_tab == "audio" and st.session_state.audio_input.strip():
    content_to_analyze = st.session_state.audio_input.strip()
elif st.session_state.active_tab == "sample" and st.session_state.sample_input.strip():
    content_to_analyze = st.session_state.sample_input.strip()
else:
    content_to_analyze = st.session_state.manual_input.strip()

if not content_to_analyze:
    content_to_analyze = (
        st.session_state.screenshot_input.strip()
        or st.session_state.audio_input.strip()
        or st.session_state.sample_input.strip()
        or st.session_state.manual_input.strip()
    )

st.session_state.input_text = content_to_analyze

if st.session_state.audit_executed and len(content_to_analyze) < 2:
    st.warning("Please provide, upload, or select advisory content to analyze.")

if st.session_state.audit_executed and len(content_to_analyze) >= 2:
    gr_check = guardrail.check_query(content_to_analyze)
    if gr_check.is_speculation_query:
        st.html("<div style='height: 1.5rem;'></div>")
        st.html(
            textwrap.dedent(
                f"""
                <div style="background: #fee2e2; border: 1px solid #f87171; border-radius: 8px; padding: 20px; margin-top: 14px;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #b91c1c; text-transform: uppercase; letter-spacing: 0.05em;">
                        ⛔ SEBI Compliance Guardrail Enforced: Speculative Request Blocked
                    </div>
                    <div style="font-size: 0.9rem; color: #7f1d1d; margin-top: 8px;">
                        <b>Query Intent:</b> {gr_check.blocked_intent}
                    </div>
                    <div style="font-size: 0.85rem; color: #991b1b; margin-top: 10px; line-height: 1.6;">
                        <b>🇮🇳 हिन्दी:</b> {gr_check.rejection_message_hindi}
                    </div>
                    <div style="font-size: 0.85rem; color: #991b1b; margin-top: 6px; line-height: 1.6;">
                        <b>🇬🇧 English:</b> {gr_check.rejection_message_english}
                    </div>
                    <div style="font-size: 0.80rem; color: #7f1d1d; margin-top: 12px; font-style: italic;">
                        SatarkBharat operates strictly as an investor defense sentinel under SEBI regulations. We do not provide stock tips, price targets, or portfolio allocation advice.
                    </div>
                </div>
                """
            )
        )
        st.stop()

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

    st.html("<div style='height: 1.5rem;'></div>")

    # Synthesize vernacular audio and escape summaries
    en_text = report.plain_english_summary
    hi_text = report.vernacular_hindi_summary
    bn_text = report.vernacular_bengali_summary

    en_audio = voice_engine.synthesize(en_text, lang="en")
    hi_audio = voice_engine.synthesize(hi_text, lang="hi")
    bn_audio = voice_engine.synthesize(bn_text, lang="bn")

    b64_en = base64.b64encode(en_audio).decode("utf-8") if en_audio else ""
    b64_hi = base64.b64encode(hi_audio).decode("utf-8") if hi_audio else ""
    b64_bn = base64.b64encode(bn_audio).decode("utf-8") if bn_audio else ""

    summaries_json = json.dumps({"en": en_text, "hi": hi_text, "bn": bn_text})

    # Main Verdict Card with Integrated Language Switcher & Subtle Speaker Icon
    st.html(
        textwrap.dedent(
            f"""
            <div class="town-list-container" style="margin-top: 10px;">
                <div class="town-list-header">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span class="town-list-title">Sentinel Audit Report</span>
                        <div class="lang-switcher">
                            <button type="button" class="lang-tab active" data-lang="en">EN</button>
                            <button type="button" class="lang-tab" data-lang="hi">हिन्दी</button>
                            <button type="button" class="lang-tab" data-lang="bn">বাংলা</button>
                        </div>
                    </div>
                    <button type="button" class="speaker-icon-btn" id="sentinel-speaker-btn" title="Listen to voice advisory" aria-label="Listen to voice advisory">
                        <div class="speaker-icon"></div>
                    </button>
                </div>

                <!-- Assessment Text & Editorial Score -->
                <div style="display: flex; align-items: center; justify-content: space-between; gap: 24px; padding: 16px 18px; background: #faf9f6; border-radius: 12px; border: 1px solid rgba(0,0,0,0.04);">
                    <div style="flex: 1;">
                        <div id="sentinel-lang-label" style="font-size: 0.74rem; font-weight: 600; text-transform: uppercase; color: #71717a; letter-spacing: 0.5px; margin-bottom: 6px;">Composite Risk Assessment · English</div>
                        <div id="sentinel-summary-text" style="font-size: 1.05rem; font-weight: 500; color: #18181b; line-height: 1.6;">{en_text}</div>
                    </div>
                    <div style="text-align: right; flex-shrink: 0; min-width: 85px; padding-left: 18px; border-left: 1px solid rgba(0,0,0,0.06);">
                        <div style="font-size: 2.2rem; font-weight: 700; color: {gauge_color}; font-family: 'Fraunces', Georgia, serif; line-height: 1;">{score}</div>
                        <div style="font-size: 0.68rem; color: #71717a; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;">out of 100</div>
                    </div>
                </div>
            </div>

            <script>
            (function() {{
                const summaries = {summaries_json};
                const audioTracks = {{
                    en: "{b64_en}" ? "data:audio/mp3;base64,{b64_en}" : "",
                    hi: "{b64_hi}" ? "data:audio/mp3;base64,{b64_hi}" : "",
                    bn: "{b64_bn}" ? "data:audio/mp3;base64,{b64_bn}" : ""
                }};
                const langNames = {{
                    en: "English",
                    hi: "हिन्दी (Hindi)",
                    bn: "বাংলা (Bengali)"
                }};

                let currentLang = "en";
                let isPlaying = false;
                let currentAudio = null;

                function init() {{
                    const btn = document.getElementById("sentinel-speaker-btn");
                    const summary = document.getElementById("sentinel-summary-text");
                    const label = document.getElementById("sentinel-lang-label");
                    const tabs = document.querySelectorAll(".lang-tab");

                    if (!btn || !summary || !label) {{
                        setTimeout(init, 50);
                        return;
                    }}

                    function stopAudio() {{
                        if (currentAudio) {{
                            currentAudio.pause();
                            currentAudio.currentTime = 0;
                        }}
                        isPlaying = false;
                        btn.classList.remove("speaking");
                    }}

                    function startAudio() {{
                        stopAudio();
                        const track = audioTracks[currentLang];
                        if (!track) return;
                        currentAudio = new Audio(track);
                        currentAudio.play().then(() => {{
                            isPlaying = true;
                            btn.classList.add("speaking");
                        }}).catch(e => {{
                            console.log("Audio play error:", e);
                            stopAudio();
                        }});
                        currentAudio.onended = function() {{
                            stopAudio();
                        }};
                    }}

                    btn.onclick = function(e) {{
                        e.preventDefault();
                        e.stopPropagation();
                        if (isPlaying) {{
                            stopAudio();
                        }} else {{
                            startAudio();
                        }}
                    }};

                    tabs.forEach(tab => {{
                        tab.onclick = function(e) {{
                            e.preventDefault();
                            e.stopPropagation();
                            tabs.forEach(t => t.classList.remove("active"));
                            this.classList.add("active");
                            const lang = this.getAttribute("data-lang");
                            currentLang = lang;
                            summary.textContent = summaries[lang] || "";
                            label.textContent = "Composite Risk Assessment · " + (langNames[lang] || lang);

                            if (isPlaying) {{
                                startAudio();
                            }} else {{
                                stopAudio();
                            }}
                        }};
                    }});
                }}

                if (document.readyState === "loading") {{
                    document.addEventListener("DOMContentLoaded", init);
                }} else {{
                    init();
                }}
            }})();
            </script>
            """
        ),
        unsafe_allow_javascript=True,
    )

    # 3. Deterministic Regulatory Invariants (Clean Typographic Presentation)
    sebi_status_class = "safe" if report.sebi_audit.is_in_registry and not report.sebi_audit.is_impersonation_suspected else ("danger" if report.sebi_audit.is_impersonation_suspected else "warning")
    sebi_status_text = "Verified Match" if sebi_status_class == "safe" else ("Impersonation Alert" if sebi_status_class == "danger" else "Unregistered")

    pay_status_class = "safe" if report.payment_audit.is_clearing_compliant else "danger"
    pay_status_text = "Clearing Compliant" if pay_status_class == "safe" else "Personal Savings VPA"

    pva_status_class = "danger" if report.guaranteed_returns_detected else "safe"
    pva_status_text = "Prohibited Return Claim" if pva_status_class == "danger" else "No Fixed Guarantees"

    dom_status_class = "danger" if report.domain_audit.is_typosquatted or report.domain_audit.has_apk_link else "safe"
    dom_status_text = "Malware / Phishing" if dom_status_class == "danger" else "Authentic Domain"

    nsdl_status_class = "danger" if report.depository_audit.is_fake_nsdl_claim else "safe"
    nsdl_status_text = "Unauthorized NSDL Claim" if nsdl_status_class == "danger" else "Depository Valid"

    st.html(
        textwrap.dedent(
            f"""
            <div class="town-list-container">
                <div class="town-list-header">
                    <span class="town-list-title">Deterministic Regulatory Invariants</span>
                    <span style="font-size: 0.8rem; color: #71717a; font-family: 'Plus Jakarta Sans', sans-serif;">5 verified benchmarks</span>
                </div>

                <!-- Item 1: SEBI Registry -->
                <div class="town-list-item">
                    <div class="town-item-content">
                        <div class="town-item-title">SEBI Intermediary Registration</div>
                        <div class="town-item-desc">Claimed ID: {report.sebi_audit.claimed_id or 'None (Unregistered)'} · Registry status: {report.sebi_audit.registry_status}</div>
                    </div>
                    <span class="invariant-status {sebi_status_class}">{sebi_status_text}</span>
                </div>

                <!-- Item 2: Payment Routing -->
                <div class="town-list-item">
                    <div class="town-item-content">
                        <div class="town-item-title">Payment Channel & Settlement Segregation</div>
                        <div class="town-item-desc">Recipient VPA: {report.payment_audit.primary_vpa or 'None specified'} · Circular 2023/71 mandate</div>
                    </div>
                    <span class="invariant-status {pay_status_class}">{pay_status_text}</span>
                </div>

                <!-- Item 3: Return Guarantee (PVA) -->
                <div class="town-list-item">
                    <div class="town-item-content">
                        <div class="town-item-title">Performance Guarantee Audit</div>
                        <div class="town-item-desc">SEBI (Research Analysts) Regulation 15(1) & PVA Code of Conduct</div>
                    </div>
                    <span class="invariant-status {pva_status_class}">{pva_status_text}</span>
                </div>

                <!-- Item 4: Domain & APK -->
                <div class="town-list-item">
                    <div class="town-item-content">
                        <div class="town-item-title">Domain Authenticity & APK Binary Invariant</div>
                        <div class="town-item-desc">Weighted Damerau-Levenshtein homoglyph distance · Section 66D IT Act</div>
                    </div>
                    <span class="invariant-status {dom_status_class}">{dom_status_text}</span>
                </div>

                <!-- Item 5: NSDL Depository -->
                <div class="town-list-item">
                    <div class="town-item-content">
                        <div class="town-item-title">NSDL Depository Invariant Safeguard</div>
                        <div class="town-item-desc">Demat account 16-character format · Depositories Act 1996 verification</div>
                    </div>
                    <span class="invariant-status {nsdl_status_class}">{nsdl_status_text}</span>
                </div>
            </div>
            """
        )
    )

    # 4. Institutional Grievance Routing (Quiet Minimalist Card)
    st.html(
        textwrap.dedent(
            f"""
            <div class="town-list-container">
                <div class="town-list-header">
                    <span class="town-list-title">Institutional Grievance Routing</span>
                    <span style="font-size: 0.8rem; color: #71717a; font-family: 'Plus Jakarta Sans', sans-serif;">{route.portal_name}</span>
                </div>
                <div style="font-size: 0.92rem; color: #18181b; line-height: 1.5; margin-bottom: 6px;">
                    <b>Statutory Basis:</b> {route.statutory_basis}
                </div>
                <div style="font-size: 0.86rem; color: #52525b; line-height: 1.5;">
                    {route.routing_rationale}
                </div>
            </div>
            """
        )
    )

    # 5. Evidentiary Exports
    if score >= 25:
        dossier_data = DossierGenerator.generate_json_dossier(report, content_to_analyze)
        pdf_bytes = DossierGenerator.generate_pdf_dossier(dossier_data)
        sms_text = DossierGenerator.generate_1930_sms(report, dossier_data["incident_id"])

        st.html(
            textwrap.dedent(
                """
                <div class="town-list-container" style="margin-bottom: 12px;">
                    <div class="town-list-header">
                        <span class="town-list-title">Evidentiary Dossier & Regulatory Dispatch</span>
                        <span style="font-size: 0.8rem; color: #71717a; font-family: 'Plus Jakarta Sans', sans-serif;">Sec 65B Indian Evidence Act compliant</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #52525b; line-height: 1.55;">
                        Generate court-ready cryptographically hashed records for official submission to <b>SEBI SCORES 2.0</b>, <b>NCRP 1930 Portal</b>, or jurisdictional Cyber Police records.
                    </div>
                </div>
                """
            )
        )

        exp_cols = st.columns(2)
        with exp_cols[0]:
            st.download_button(
                label="📄 Download PDF Dossier (Court-Ready)",
                data=pdf_bytes,
                file_name=f"Satark_Dossier_{dossier_data['incident_id']}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        with exp_cols[1]:
            st.download_button(
                label="💾 Download Structured JSON (SCORES / NCRP)",
                data=json.dumps(dossier_data, indent=2),
                file_name=f"Satark_Dossier_{dossier_data['incident_id']}.json",
                mime="application/json",
                use_container_width=True,
            )

        st.html(
            textwrap.dedent(
                f"""
                <details class="sms-dispatch-details">
                    <summary class="sms-dispatch-summary">
                        <span style="font-size: 0.86rem; font-weight: 600; color: #18181b;">1930 Cyber Fraud Helpline Dispatch Template</span>
                        <span style="font-size: 0.74rem; font-weight: 500; color: #71717a;">Click to expand</span>
                    </summary>
                    <div class="sms-dispatch-body">
                        <div style="font-size: 0.78rem; color: #71717a; margin-bottom: 8px;">Pre-formatted statutory text ready for instant transmission to NCRP 1930 operators:</div>
                        <pre class="sms-dispatch-pre">{sms_text}</pre>
                    </div>
                </details>
                """
            )
        )
    else:
        st.html(
            textwrap.dedent(
                """
                <div class="town-list-container" style="margin-bottom: 12px; background: #ecfdf5; border: 1px solid #a7f3d0;">
                    <div class="town-list-header">
                        <span class="town-list-title" style="color: #065f46;">✅ Verified Invariants / No Action Required</span>
                        <span style="font-size: 0.8rem; color: #047857; font-family: 'Plus Jakarta Sans', sans-serif;">SEBI & IT Act Invariants Cleared</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #065f46; line-height: 1.55;">
                        No illegal promises of guaranteed return, unofficial APK downloads, or personal payment collections were detected. No complaint filing or regulatory escalation is required.
                    </div>
                </div>
                """
            )
        )

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.html("<div style='height: 3.5rem;'></div>")
st.html(
    textwrap.dedent(
        """
        <div style="text-align: center; border-top: 1px solid rgba(0, 0, 0, 0.06); padding-top: 2rem; font-size: 0.80rem; color: #a1a1aa;">
            SatarkBharat · Built for SANGYAN (SNTC, IIT BHU Varanasi × SEBI × NSDL) · Zero Stock Tips · 100% Investor Defense
        </div>
        """
    )
)
