"""Configuration constants, file paths, and Town-inspired design palette for SatarkBharat."""

import os
import re
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"

SEBI_REGISTRY_PATH = DATA_DIR / "sebi_registry_snapshot.json"
VERIFIED_DOMAINS_PATH = DATA_DIR / "verified_brokers_domains.json"
SAMPLES_PATH = DATA_DIR / "samples" / "scenarios.json"

# Regulatory Penalties (Mathematical Weights)
PENALTY_WEIGHTS = {
    "GUARANTEED_RETURNS": 35,
    "INVALID_SEBI_ID": 30,
    "SEBI_SPOOF_IMPERSONATION": 40,
    "PERSONAL_UPI_PAYMENT": 25,
    "TYPOSQUATTED_DOMAIN": 30,
    "UNOFFICIAL_APK_LINK": 40,
    "URGENCY_FOMO_COERCION": 15,
    "UNREGISTERED_FUND_POOL": 35,
}

# SEBI Registration Patterns (Compiled Regex AST)

SEBI_PATTERNS = {
    "RESEARCH_ANALYST": re.compile(r"^INH\d{9}$"),
    "INVESTMENT_ADVISER": re.compile(r"^INA\d{9}$"),
    "STOCK_BROKER": re.compile(r"^INZ\d{9}$"),
    "MERCHANT_BANKER": re.compile(r"^INM\d{9}$"),
    "PORTFOLIO_MANAGER": re.compile(r"^INP\d{9}$"),
    "MUTUAL_FUND": re.compile(r"^MF\/\d{3}\/\d{2}\/\d{2}$"),
}

SEBI_GENERAL_REGEX = re.compile(r"\b(IN[AHZMP]\d{9}|MF\/\d{3}\/\d{2}\/\d{2})\b", re.IGNORECASE)
UPI_VPA_REGEX = re.compile(r"\b([a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64})\b")
URL_REGEX = re.compile(r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
APK_REGEX = re.compile(r"\b[\w\-.]+\.apk\b|download\.apk|app\.trade", re.IGNORECASE)

# Town-Inspired Design Palette (Deep Charcoal Obsidian, Warm Carbon, Gold Accent)
TOWN_THEME = {
    "bg_primary": "#161614",          # Deep warm obsidian (Town canvas)
    "bg_card": "#1f1f1c",             # Elevated card surface
    "bg_subtle": "#272723",           # Interactive pill & input background
    "border_ghost": "rgba(255, 255, 255, 0.08)", # Subtle hairline border
    "border_focus": "rgba(255, 255, 255, 0.20)",
    "text_primary": "#f5f5f3",        # High readability off-white
    "text_muted": "#a1a19a",          # Subdued description gray
    "accent_gold": "#e5a93b",         # Satark alert gold / brand highlight
    "status_safe": "#34d399",         # Emerald green for verified status
    "status_caution": "#fbbf24",      # Amber for caution
    "status_danger": "#f87171",       # Crimson coral for critical risk
}


def get_telegram_bot_token() -> str | None:
    """Retrieve Telegram Bot Token from environment or project .env file."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if token:
        return token.strip()
    env_paths = [PROJECT_ROOT / ".env", Path(".env")]
    for env_path in env_paths:
        if env_path.exists():
            try:
                for line in env_path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line.startswith("TELEGRAM_BOT_TOKEN="):
                        return line.split("=", 1)[1].strip()
            except Exception:
                pass
    return None


def get_gemini_api_key() -> str | None:
    """Retrieve Gemini API key from environment, Streamlit secrets, or project .env file."""
    try:
        import streamlit as st

        if hasattr(st, "secrets"):
            if "GEMINI_API_KEY" in st.secrets:
                return str(st.secrets["GEMINI_API_KEY"]).strip()
            if "GOOGLE_API_KEY" in st.secrets:
                return str(st.secrets["GOOGLE_API_KEY"]).strip()
    except Exception:
        pass

    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key.strip()

    env_paths = [PROJECT_ROOT / ".env", Path(".env")]
    for env_path in env_paths:
        if env_path.exists():
            try:
                for line in env_path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY="):
                        return line.split("=", 1)[1].strip()
                    if line.startswith("GOOGLE_API_KEY="):
                        return line.split("=", 1)[1].strip()
            except Exception:
                pass
    return None
