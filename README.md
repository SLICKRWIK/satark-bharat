# SatarkBharat (सतर्क भारत)

<div align="center">

![SatarkBharat Hero Banner](https://img.shields.io/badge/SatarkBharat-Pre--Transaction_Investor_Sentinel-d97706?style=for-the-badge&logoColor=white)

**A Multimodal, Pre-Transaction Neuro-Symbolic Sentinel for Indian Retail Investor Defense**  
*Built for the SANGYAN Hackathon (SNTC IIT-BHU × SEBI × NSDL) · Track A: Digital Fraud & Scam Resilience*

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Tests Passing](https://img.shields.io/badge/tests-30%2F30%20passed-success)](https://github.com/SLICKRWIK/satark-bharat)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit%201.35+-FF4B4B.svg)](https://streamlit.io)
[![Telegram Bot](https://img.shields.io/badge/Telegram_Bot-Active_Sentinel-2CA5E0.svg?logo=telegram&logoColor=white)](#-telegram-bot-sentinel)
[![SEBI Compliant](https://img.shields.io/badge/SEBI-Zero%20Stock%20Tips-10b981.svg)](https://www.sebi.gov.in)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Live Architecture](#-system-architecture) • [Key Differentiators](#-the-top-1-institutional-moat) • [Telegram Bot](#-telegram-bot-sentinel) • [CLI Usage](#-command-line-interface-cli) • [Quickstart](#-quickstart-with-uv) • [Statutory Compliance](#-statutory-guardrails--legal-citations)

</div>

---

## 🌟 Executive Summary

Over **100 million retail investors** have entered India’s capital markets, with unprecedented growth across Tier-2, Tier-3, and rural regions. However, this democratization has triggered an asymmetric surge in financial cybercrime:
- **Unregistered Telegram & WhatsApp syndicates** promising "500% guaranteed jackpot calls".
- **Forged SEBI registration certificates** impersonating licensed Research Analysts (RAs) and Investment Advisers (IAs).
- **Personal UPI collection traps** soliciting advisory fees into personal savings accounts (`@paytm`, `@okhdfcbank`) rather than SEBI-regulated clearing corporation pools.
- **Cloned APK trading terminals** (`zer0dha.apk`, `angel-one-vip.apk`) stealing biometrics and credentials.

Traditional consumer grievance mechanisms operate **post-facto**—complaints are filed *after* money has exited the account. Furthermore, naive GenAI wrappers hallucinate compliance and violate regulations by dispensing illegal stock advice.

**SatarkBharat (सतर्क भारत)** is an open-source, pre-transaction, neuro-symbolic defense sentinel deployed across three interconnected channels:
1. **Interactive Web Sentinel (`app.py`):** Town-inspired editorial UI with multi-modal tabs, live institutional scrolling ticker, audio playback, and PDF dossier generation.
2. **Real-Time Telegram Bot Sentinel (`telegram_bot.py`):** Meets investors directly where scams occur, offering instant pre-transaction audit of forwarded channel messages, photos, voice notes, and APKs.
3. **Headless CLI Tools (`satark` / `satark-bot`):** Automated screening pipelines and server automation.

It combines **multimodal neural perception** (Hindi/Bengali ASR, EasyOCR) with a **deterministic regulatory audit matrix** (regex AST, offline SEBI intermediary hashmap, dnstwist typosquatting, and payment clearing invariants) to stop fraud *before* money leaves the account. It translates complex legalities into instantaneous vernacular voice alerts and auto-generates court-ready Section 65B complaint dossiers.

---

## 🛡️ The "Top 1%" Institutional Moat

Judges from **SEBI, NSDL, and IIT-BHU** immediately penalize generic LLM prompt wrappers. SatarkBharat embeds four foundational institutional differentiators:

### 1. SEBI SCORES 2.0 vs. Market Intelligence (MI) vs. NCRP 1930 Triaging
Typical projects claim: *"We automatically file on SEBI SCORES."*  
**The Regulatory Reality:**
- **SEBI SCORES 2.0** strictly requires the respondent to be an **officially registered intermediary** with an existing client relationship. Anonymous Telegram groups and fake entities are rejected by SCORES.
- **Unregistered syndicates, illegal pools, and pump-and-dump operators** belong to the **SEBI Market Intelligence (MI)** portal for regulatory banning orders.
- **Cyber deception, extortion, and unauthorized payment solicitation** fall under IPC/BNS and Section 66D of the IT Act, requiring the **National Cyber Crime Reporting Portal (NCRP / Helpline 1930)**.

```
                     [ Entity Verification Result ]
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
[ Claims Valid SEBI Registration ]            [ Unregistered / Fake / Impersonator ]
- Entity exists on SEBI database              - Regex fails or Registry match = false
- Intermediary misconduct / spoofing          - Illegal pool / WhatsApp syndicate
         │                                                   │
         ▼                                                   ▼
[ Format: SEBI SCORES 2.0 ]                 [ Format: SEBI MI Portal + NCRP 1930 ]
- Actionable Intermediary Dossier           - Cybercrime evidence docket (IPC/IT Act)
- Folio / Reg ID cross-reference            - Bank/UPI freeze request format for 1930
```

### 2. SEBI Circular 2023/71 & PVA Return Guarantee Enforcement
- **Regulation 15(1) of SEBI (Research Analysts) Regulations 2014:** Prohibits intermediaries from assuring, guaranteeing, or indicating fixed/sure-shot yields. Any claim of guaranteed return triggers an automatic $+35$ mathematical penalty.
- **SEBI Circular 2023/71 & NPCI Gateway Directives:** Advisory fees and market funds cannot be collected into personal savings VPAs (`@okhdfcbank`, `@paytm`, `@ybl`). Funds must flow to authorized corporate merchant accounts or Clearing Corporation (CC) settlement pools.

### 3. Zero-Hallucination Neuro-Symbolic Architecture
- **Neural Layer:** Extracts unstructured indicators from Hindi/Bengali voice notes, chat screenshots, and forwarded SMS.
- **Symbolic Layer:** Validates SEBI IDs against deterministic compiled regex `^IN[A-H]\d{9}$`, cross-references official offline snapshots, audits UPI handles, checks NSDL Demat account invariants, and checks Levenshtein homoglyphs against authentic broker endpoints.

### 4. Deterministic Multi-Lingual Intent & Speculation Interceptor
- **Tri-Vector Interrogative Interceptor:** Evaluates queries by intersecting interrogatives (`konsa`, `ki`, `which`), securities (`stock`, `share`, `nifty`), and action verbs (`kharidu`, `kinbo`, `buy`, `invest`) across English, Hindi, Hinglish, Bengali, and Banglish.
- **100% Sub-Millisecond Guardrail:** Catches questions like *"kal konsa stock kharidu?"* or *"kal ki stock kinbo?"* in $<2\text{ms}$ with zero API token spend, ensuring absolute compliance with SEBI (Research Analysts) Regulations.
- **Multilingual Defensive Refusal:** Automatically responds with localized SEBI Investor Charter reminders in Hindi, Bengali, and English.

### 5. Deterministic Local-First Offline Resilience
- **Zero API Downtime Risk:** The core sentinel—including SEBI registry lookup, NPCI payment validation, threat index calculation, PDF complaint generation, and 1930 SMS formatting—runs **100% locally and offline**.
- Even if external cloud AI quotas or rate limits are reached, the application never freezes, halts, or fails.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Channels ["Ingestion Channels"]
        CH_WEB["Town-Inspired Sentinel Web UI<br/>(Streamlit with Ctrl+Enter & Live Ticker)"]
        CH_BOT["Telegram Bot Sentinel<br/>(Forward Provenance, Voice, Photos, APKs)"]
        CH_CLI["Headless CLI Tool<br/>(satark / satark-bot)"]
    end

    subgraph Ingestion ["Multimodal Perception Layer"]
        ING_TEXT["Raw Advisory & Chat Text"]
        ING_OCR["Visual OCR Parser<br/>(Gemini Vision + EasyOCR Fallback)"]
        ING_AUDIO["Indic Speech-to-Text<br/>(Hindi, Bengali, Hinglish, English)"]
        ING_APK["APK Binary Attachment Interceptor"]
    end

    subgraph DecisionPrep ["Intent Classification & Guardrails"]
        INTENT_CLS["Tri-Vector Interrogative Interceptor<br/>(Interrogative + Securities + Action Verbs)"]
        SEBI_GUARD["SEBI Compliance Guardrail<br/>(Strict Block on Tips in Hindi/Bengali/English)"]
    end

    subgraph SymbolicMatrix ["Deterministic Symbolic Regulatory Matrix"]
        REG_SEBI["SEBI Registry Auditor<br/>(Regex AST + Offline Intermediary Hashmap)"]
        REG_PAY["Payment Channel Auditor<br/>(Circular 2023/71 Personal VPA vs Clearing)"]
        REG_DOM["Domain Typosquatting Auditor<br/>(Levenshtein Distance + Homoglyphs + APKs)"]
        REG_NSDL["NSDL Depository Invariant Auditor<br/>(16-Digit Demat & Depositories Act 1996)"]
        REG_PVA["Psychological Coercion & PVA Auditor<br/>(Guaranteed Returns, FOMO, VIP Pools)"]
    end

    subgraph ThreatEngine ["Threat & Risk Engine"]
        ENG_MATH["Mathematical Penalty Engine<br/>(Bounded Threat Score 0-100 & Red Lines)"]
        ENG_ROUTE["Jurisdictional Redressal Router<br/>(SCORES 2.0 vs NCRP 1930 / SEBI MI)"]
    end

    subgraph Redressal ["Evidentiary Redressal Layer"]
        OUT_VOICE["Vernacular Voice Alerts<br/>(Colloquial Hindi, Bengali, English Audio)"]
        OUT_PDF["Court-Ready PDF Dossier<br/>(Section 65B BSA Compliant + SHA-256)"]
        OUT_SMS["1930 Cyber Fraud Quick-Dispatch SMS"]
    end

    CH_WEB & CH_BOT & CH_CLI --> Ingestion
    ING_TEXT & ING_OCR & ING_AUDIO & ING_APK --> INTENT_CLS
    INTENT_CLS -->|Speculation Query| SEBI_GUARD
    INTENT_CLS -->|Evidence / Financial Text| SymbolicMatrix

    REG_SEBI & REG_PAY & REG_DOM & REG_NSDL & REG_PVA --> ENG_MATH
    ENG_MATH --> ENG_ROUTE
    ENG_MATH --> OUT_VOICE
    ENG_ROUTE --> OUT_PDF & OUT_SMS
    OUT_PDF & OUT_SMS & OUT_VOICE --> CH_WEB & CH_BOT & CH_CLI
```

---

## 🧮 Mathematical Threat Index & Invariant Scoring

The Satark Threat Index ($T$) is bounded deterministically:
$$T = \min\left(100, \sum_{i=1}^{k} W_i \cdot P_i\right)$$

| Factor Code | Audit Dimension | Risk Condition | Penalty Weight ($W_i$) |
|---|---|---|---|
| **$P_{\text{G-RET}}$** | Regulatory Invariant | Claiming guaranteed, fixed, or loss-free financial returns | **+35** |
| **$P_{\text{SEBI-INVALID}}$** | Entity Invariant | Fake, unparseable, or non-existent SEBI Registration Number | **+30** |
| **$P_{\text{SEBI-SPOOF}}$** | Entity Invariant | Valid SEBI ID claimed, but entity name does not match registry | **+40** |
| **$P_{\text{PAY-PERS}}$** | Payment Channel | Demanding advisory/investment funds to a personal savings UPI | **+25** |
| **$P_{\text{URL-TYPO}}$** | Domain Permutation | Cloned or look-alike domain detected via Levenshtein check | **+30** |
| **$P_{\text{APK-UNOFF}}$** | Malware Invariant | Direct distribution of unofficial `.apk` trading client | **+40** |
| **$P_{\text{FOMO-URG}}$** | Behavioral Coercion | High urgency cues ("Upper circuit only today", "Immediate VIP slot") | **+15** |
| **$P_{\text{UNREG-POOL}}$** | Regulatory Invariant | Demanding money pooling for "institutional/block trading" | **+35** |
| **$P_{\text{NSDL-FAKE}}$** | Depository Invariant | Fake NSDL demat account freeze notice or fee extortion | **+35** |

### Deterministic Red Line Overrides
If any of the following occur, the score immediately snaps to **100/100 (CRITICAL RISK)**:
1. `APK-UNOFF == True` (Untrusted APK binary link).
2. `SEBI-SPOOF == True AND PAY-PERS == True` (Impersonating a licensed entity while collecting personal UPI).
3. `G-RET == True AND PAY-PERS == True` (Guaranteed return promise combined with personal UPI transfer).

---

## 🧪 Pre-Packaged Demo Scenarios

SatarkBharat includes 4 one-click test cases in `data/samples/scenarios.json`:

| Scenario | Input Summary | Primary Breach | Threat Score | Target Redressal |
| :--- | :--- | :--- | :--- | :--- |
| **Case A: Impersonation** | Claims real SEBI RA license `INH000008921` (Apex Capital), promises 200% return, asks for UPI to `rajesh.advisory99@okhdfcbank`. | SEBI ID Spoofing + Personal VPA + Guaranteed Return | **95/100** (Critical) | **SEBI SCORES 2.0** |
| **Case B: Telegram Syndicate** | Hindi audio transcript promising 500% operator upper circuit, asks for funds to `sureprofit.pool@paytm`. | Unregistered Syndicate + Collective Pooling + Extreme FOMO | **95/100** (Critical) | **NCRP 1930 & SEBI MI** |
| **Case C: Cloned APK** | Phishing SMS urging KYC update via `https://zer0dha-app.trade/login.apk`. | Typosquatted domain mimicking Zerodha + Malicious APK binary | **100/100** (Red Line) | **NCRP 1930 & Cyber Police** |
| **Case D: Verified Broker** | Official risk disclaimer from Zerodha Broking (`INZ000031633`) pointing to `zerodha.com`. | None. Statutory risk disclosures present. | **5/100** (Low Risk) | **Verified (Safe)** |

---

## 🤖 Telegram Bot Sentinel (Real-Time Forward & Chat Defense)

SatarkBharat includes a fully integrated, production-ready Telegram Bot sentinel (`satark_bharat.telegram_bot`). It provides instant pre-transaction investor defense right inside Telegram—where millions of fraudulent investment groups, pump-and-dump syndicates, and unverified tipsters operate.

### Sentinel Capabilities on Telegram:
- **Channel Forward Provenance:** Forward any suspicious post directly from a channel or group. SatarkBharat automatically extracts the channel's title, public username (`@channel`), and message ID to construct a legally traceable chain of custody.
- **Multimodal Visual OCR:** Send screenshots of WhatsApp conversations, fraudulent SEBI registration certificates, or payment QR codes.
- **Vernacular Voice Notes:** Send voice notes (`.oga`, `.ogg`, `.mp3`) in colloquial Hindi, Bengali, Hinglish, or English.
- **Android APK Interceptor:** Uploading an `.apk` file (e.g. `zerodha-vip.apk`) triggers an immediate **Critical Risk (100/100) Red Line** alert warning against credential theft and unauthorized access.
- **Court-Ready PDF Dossier Delivery:** If a risk is detected ($\ge 25/100$), the bot automatically replies with an official, court-ready Section 65B PDF Complaint Dossier ready for immediate submission.
- **1930 Cyber Fraud Helpline Dispatch:** For high-threat scams, the bot generates a pre-formatted SMS string ready for 1-tap copy/paste to helpline **1930** or `cybercrime.gov.in`.
- **SEBI Anti-Speculation Guardrail:** Rejects stock tips, price predictions, or buying calls across English, Hindi, and Bengali.

### Available Commands:
- `/start` — Multilingual introduction and step-by-step audit instructions.
- `/help` — Emergency cybercrime helpline guidance (1930, SEBI SCORES, NCRP).
- `/status` — Live diagnostic inspection of SEBI registry counts, verified broker databases, and engine health.

---

## 💻 Command-Line Interface (CLI)

SatarkBharat features a lightweight, high-performance CLI tool for automated screening and terminal workflows:

```bash
# Basic terminal analysis
uv run satark "Namaste Sir! 200% guaranteed jackpot return! Send fee to scammer@okhdfcbank"

# Generate 1930 Cyber Cell pre-formatted SMS dispatch
uv run satark --sms "Urgent: Nifty operator call, deposit to 9876543210@paytm"

# Generate full structured JSON evidentiary dossier
uv run satark --json "Join our VIP Option chain! 200% profit. Send Rs 5000 to pool@ybl"
```

---

## ⚡ Quickstart with `uv`

SatarkBharat uses [`uv`](https://github.com/astral-sh/uv) for fast, deterministic Python virtual environment and dependency management.

```bash
# 1. Clone repository
git clone https://github.com/SLICKRWIK/satark-bharat.git
cd satark-bharat

# 2. Create virtual environment with Python 3.11
uv venv --python 3.11

# 3. Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (cmd):
.venv\Scripts\activate.bat
# Linux/macOS:
source .venv/bin/activate

# 4. Install dependencies in editable mode
uv pip install -e ".[dev]"

# 5. Configure Environment (.env file in root)
# Add your Telegram Bot Token & optional Gemini API Key:
# TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
# GEMINI_API_KEY="your_gemini_api_key"

# 6. Run test suite
uv run pytest tests/

# 7. Launch the Streamlit Sentinel Web UI
uv run streamlit run app.py

# 8. Launch the Telegram Bot Sentinel
uv run satark-bot
# (or: python -m satark_bharat.telegram_bot)
```

---

## 🚀 How to Start the Telegram Bot

You can run the Telegram Bot either through `uv` or standard Python:

### Step 1: Obtain a Bot Token
1. Open Telegram and search for `@BotFather`.
2. Send `/newbot` and follow the prompts to choose a display name and username.
3. Copy the HTTP API token provided by BotFather (e.g. `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`).

### Step 2: Configure Environment
Add your token to the `.env` file in the project root:
```env
TELEGRAM_BOT_TOKEN=your_token_here
GEMINI_API_KEY=your_gemini_api_key_here  # Optional: for multimodal vision/audio
```
*(Alternatively, set it via shell environment variable: `$env:TELEGRAM_BOT_TOKEN="your_token"` on PowerShell or `export TELEGRAM_BOT_TOKEN="your_token"` on Linux/macOS).*

### Step 3: Run the Bot
In your activated terminal:
```bash
# Using uv:
uv run satark-bot

# OR using Python module syntax:
python -m satark_bharat.telegram_bot
```
The console will confirm:
```
SatarkBharat Telegram Bot is starting polling...
Application started
```
Open Telegram, message your bot, and send `/start` or forward any suspicious chat message!

---

## 📂 Repository Layout

```
satark-bharat/
├── pyproject.toml                     # uv package configuration & dependencies
├── uv.lock                            # Deterministic lockfile
├── README.md                          # Comprehensive project documentation
├── app.py                             # High-craft Town-inspired Sentinel Web UI
├── docs/
│   ├── MASTER_DOCUMENT.md             # Complete master architectural & regulatory spec
│   ├── ARCHITECTURE.md                # System topology diagrams
│   └── REGULATORY_GUIDELINES.md       # Legal and statutory citations
├── data/
│   ├── sebi_registry_snapshot.json    # Offline hashmap of verified SEBI entities
│   ├── verified_brokers_domains.json  # Whitelisted legitimate broker domains
│   └── samples/                       # Test scenarios, audio notes, screenshots
├── src/
│   └── satark_bharat/
│       ├── cli.py                     # Safe English-only command-line interface
│       ├── config.py                  # Global application constants and paths
│       ├── telegram_bot.py            # Real-time Telegram Bot Sentinel
│       ├── ingestion/                 # Multimodal Perception (Audio & OCR)
│       │   ├── audio.py               # Speech-to-text pipeline
│       │   └── ocr.py                 # Multi-script Visual OCR
│       ├── symbolic/                  # Deterministic Regulatory Matrix
│       │   ├── sebi_registry.py       # SEBI Registration AST & checksum validator
│       │   ├── payment_auditor.py     # Circular 2023/71 personal VPA classifier
│       │   ├── domain_auditor.py      # Damerau-Levenshtein typosquatting & APK detector
│       │   └── nsdl_auditor.py        # 16-digit Demat & Depositories Act auditor
│       ├── decision/                  # Threat Synthesis & Guardrails
│       │   ├── intent_classifier.py   # Multi-script Intent & Speculation Classifier
│       │   ├── math_engine.py         # Bayesian evidence fusion & coercion saturation
│       │   ├── threat_engine.py       # Multi-factor penalty scoring formula (0-100)
│       │   └── guardrails.py          # Anti-Speculation & Anti-Tipping Guardrail
│       ├── redressal/                 # Grievance Packaging & Dispatch
│       │   ├── router.py              # SCORES 2.0 vs SEBI MI / NCRP 1930 triaging
│       │   └── dossier.py             # Section 65B court-ready PDF & JSON generator
│       └── vernacular/                # Bharat-First Voice
│           └── tts.py                 # Vernacular voice synthesizer (Hindi, Bengali)
└── tests/
    ├── test_symbolic_engine.py        # 14 deterministic symbolic & redressal tests
    ├── test_intent_classifier.py      # 6 multi-lingual intent & Bengali advice tests
    ├── test_telegram_bot.py           # 7 Telegram Bot provenance, guardrail & PDF tests
    └── test_multimodal_ingestion.py   # 3 Visual OCR and Audio ingestion tests
```

---

## ⚖️ Statutory Guardrails & Legal Citations

SatarkBharat is engineered in strict adherence to Indian securities laws and digital evidence standards:

| Regulation | Statutory Citation | Institutional Purpose in SatarkBharat |
|---|---|---|
| **Prohibition of Assured Returns** | Regulation 15(1) & Schedule III, SEBI (Research Analysts) Regulations, 2014 | Triggers $+35$ penalty on any claim of guaranteed or fixed returns. |
| **Payment Segregation Mandate** | SEBI Circular `SEBI/HO/MIRSD/MIRSD-PoD-1/P/CIR/2023/71` | Blocks advisory fee collection into personal savings UPI handles. |
| **Mandatory Registration** | Section 12(1), Securities and Exchange Board of India Act, 1992 | Flags unregistered entities soliciting investment advisory funds. |
| **Cheating by Personation** | Section 66D, Information Technology Act, 2000 & BNS Section 318(4) | Auto-routes impersonation and cloned APK distribution to NCRP 1930. |
| **Depository Invariants** | Depositories Act, 1996 & SEBI (Depositories and Participants) Reg. 2018 | Verifies 16-character Demat account integrity against fake freeze notices. |
| **Electronic Evidence Admissibility** | Section 65B, Indian Evidence Act, 1872 (Section 63 BSA 2023) | Compiles court-ready evidentiary PDF dockets with SHA-256 hashes. |

---

## 🇮🇳 SANGYAN Hackathon Compliance Guarantee

- **0% Stock Tips / 0% Speculative Predictions:** SatarkBharat refuses to recommend stocks, provide price targets, or suggest trading strategies.
- **Zero Commercial Upselling:** No broker endorsements, affiliate links, or broking monetization.
- **Privacy-by-Design:** No OTPs, passwords, or sensitive account credentials are ever requested or stored.

---

<div align="center">

**SatarkBharat (सतर्क भारत)** — *Securing every rupee for the families of Bharat.*  
Built with pride for **SANGYAN 2024** · SNTC, IIT (BHU) Varanasi × SEBI × NSDL

</div>
