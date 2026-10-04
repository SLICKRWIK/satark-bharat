# SatarkBharat — Developer & AI Agent Guidelines (`agent.md`)

> **Project:** SatarkBharat (सतर्क भारत) — Pre-Transaction Multimodal Investor Defense Sentinel  
> **Context:** IIT-BHU × SEBI × NSDL Hackathon  
> **Target Audience:** Tier-2, Tier-3, and First-Time Indian Retail Investors  
> **Core Principle:** Hybrid Neuro-Symbolic Verification (Zero Hallucination + Zero Stock Advice)

---

## 1. Agent Persona & Working Philosophy

As an AI engineering agent working on SatarkBharat:
1. **Regulatory Precision Over Hype:** Never generate probabilistic guesses when deterministic rules exist. A SEBI registration number either matches `^IN[A-H]\d{9}$` and the official registry or it does not.
2. **Absolute Guardrail Compliance:** Under NO circumstances may this application provide stock picks, market forecasts, portfolio rebalancing advice, or buy/sell calls. Any such prompt must be firmly intercepted and refused with an investor charter reminder.
3. **Bharat-First Accessibility:** The end user is not a Dalal Street broker; they are everyday citizens in Lucknow, Howrah, or Solapur receiving forwarded Telegram messages and Hindi/Bengali voice notes. Explanations must be free of legalistic jargon, clear, and audio-first.
4. **Institutional Accuracy:** Maintain the crucial distinction between **SEBI SCORES 2.0** (registered entity grievances) vs. **SEBI Market Intelligence (MI) Portal** and **NCRP 1930** (unregistered criminal scams / cyber fraud).

---

## 2. Environment & Dependency Management (`uv`)

This project strictly utilizes **`uv`** as its single tool for Python version management, virtual environments, and dependency resolution.

### Common Commands
- **Python Version:** Python 3.11 (`uv python pin 3.11`)
- **Virtual Environment:** `uv venv`
- **Activate:** `source .venv/bin/activate`
- **Install Dependencies:** `uv pip install -e .` or `uv sync`
- **Run Application:** `uv run streamlit run app.py`
- **Run Tests:** `uv run pytest tests/`
- **Format & Lint:** `uv run ruff check .` / `uv run ruff format .`

> **Rule:** Never use standard `pip` or `conda` directly; always run through `uv`.

---

## 3. Directory Layout Standard

```
satark-bharat/
├── pyproject.toml                     # Modern UV-managed build configuration
├── uv.lock                            # Deterministic lockfile
├── .python-version                    # Pinned Python version (3.11)
├── agent.md                           # Universal developer & AI agent guidelines (this file)
├── gemini.md                          # Gemini multimodal prompt & schema specification
├── guardrails.md                      # Statutory SEBI & NPCI regulatory invariants
├── README.md                          # Hackathon pitch & quickstart
├── docs/
│   ├── MASTER_DOCUMENT.md             # Complete master architectural specification
│   ├── ARCHITECTURE.md                # System topology diagrams
│   └── REGULATORY_GUIDELINES.md       # Legal and statutory citations
├── data/
│   ├── sebi_registry_snapshot.json    # Offline hashmap of verified SEBI entities
│   ├── verified_brokers_domains.json  # Whitelisted legitimate broker domains
│   └── samples/                       # Pre-packaged test scams (screenshots, audio, text)
├── src/
│   └── satark_bharat/
│       ├── __init__.py
│       ├── config.py                  # Global application constants and paths
│       ├── ingestion/                 # Multimodal perception
│       │   ├── audio.py               # Speech-to-text with local/cloud fallback
│       │   └── ocr.py                 # EasyOCR / image text extractor
│       ├── symbolic/                  # Deterministic regulatory rules
│       │   ├── sebi_registry.py       # Regex AST & hashmap validator
│       │   ├── payment_auditor.py     # UPI VPA personal vs clearing pool classifier
│       │   └── domain_auditor.py      # dnstwist / Levenshtein permutation engine
│       ├── decision/                  # Risk synthesis
│       │   ├── threat_engine.py       # Mathematical penalty scoring (0-100)
│       │   └── guardrails.py          # Anti-speculation mathematical blocks
│       ├── redressal/                 # Grievance packaging
│       │   ├── router.py              # SCORES 2.0 vs SEBI MI / NCRP 1930 triaging
│       │   └── dossier.py             # Structured JSON & PDF generator
│       └── vernacular/                # Audio response
│           └── tts.py                 # Vernacular voice synthesizer (Hindi, Bengali)
├── app.py                             # Ultra-minimalist Town-inspired web sentinel
└── tests/                             # Pytest suite
    ├── __init__.py
    └── test_symbolic_engine.py
```

---

## 4. Deterministic Invariant Rules

Every agent modifying code in `src/satark_bharat/symbolic/` must preserve these invariant invariants:

1. **SEBI Registration ID Patterns:**
   - Research Analyst: `^INH\d{9}$`
   - Investment Adviser: `^INA\d{9}$`
   - Stock Broker: `^INZ\d{9}$`
   - Merchant Banker: `^INM\d{9}$`
   - Portfolio Manager: `^INP\d{9}$`
   - Mutual Fund: `^MF\/\d{3}\/\d{2}\/\d{2}$`
2. **Guaranteed Returns = Instant Severe Violation:**
   - Any claim of `guaranteed`, `fixed`, `loss-free`, or `sure-shot` returns carries an automatic $+35$ penalty points under SEBI RA Regulations 2014 Reg 15(1).
3. **Personal VPA Destination:**
   - Payments solicited to personal handles (`@okhdfcbank`, `@okaxis`, `@ybl`, `@paytm`, `@ibl`, `@apl`) rather than SEBI-approved clearing corporations or corporate merchant VPAs trigger an automatic $+25$ penalty.
4. **Immediate Red Line Override:**
   - If an unauthorized `.apk` link is detected or an authentic SEBI entity is spoofed with an alien payment account, the composite threat score snaps directly to **100/100 (CRITICAL RISK)**.

---

## 5. UI & Aesthetic Philosophy (Town Inspiration)

The UI must follow the aesthetic principles of modern, high-craft web software (inspired by `data/webste_inspiration`):
- **Minimalist Canvas:** No clunky left or right sidebars eating up screen real estate. Single, elegant centered column.
- **Palette:** Warm dark obsidian background (`#161614` / `#181816`), subtle card surfaces (`#20201d` / `#242421`), delicate hairline borders (`rgba(255, 255, 255, 0.08)`).
- **Floating Controls:** Squircle navigation pill (`border-radius: 12px`), smooth status tags, non-blocky inputs.
- **Micro-Interactions:** One-click sample loaders (Case A, Case B, Case C) for instant judge demonstrations; smooth toggle drawers for deep evidence audit.
