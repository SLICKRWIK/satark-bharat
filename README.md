# SatarkBharat (सतर्क भारत)

> **Multimodal, Pre-Transaction Neuro-Symbolic Sentinel for Indian Retail Investor Defense**  
> *Built for IIT-BHU × SEBI × NSDL Hackathon*

---

## 🌟 Executive Overview

**SatarkBharat** protects Tier-2, Tier-3, and first-time Indian retail investors against fraudulent advisory syndicates, fake SEBI letterheads, cloned APK trading apps, and deceptive personal UPI collection channels before money leaves their accounts.

Unlike naive LLM wrappers that hallucinate regulatory compliance, SatarkBharat combines:
1. **Multimodal Ingestion:** Handles vernacular Hindi/Bengali voice notes, Telegram/WhatsApp chat screenshots, and Hinglish advisory texts.
2. **Deterministic Regulatory Symbolic Matrix:** Zero-hallucination validation via regex AST, offline SEBI intermediary hashmap, payment clearing invariants, and `dnstwist` domain typosquatting detection.
3. **Institutional Redressal Triaging:** Automatically bifurcates grievances into **SEBI SCORES 2.0** (for registered entity impersonation) vs. **SEBI Market Intelligence (MI)** and **NCRP 1930 / cybercrime.gov.in** (for unregistered criminal fraud).
4. **Town-Inspired Minimalist Web UI:** Clean, fluid, clutter-free single-column design with zero bulky sidebars.

---

## ⚡ Quickstart with `uv`

SatarkBharat uses [`uv`](https://github.com/astral-sh/uv) for fast, deterministic Python environment and dependency management.

```bash
# 1. Clone repository
git clone https://github.com/satark-bharat/satark-bharat.git
cd satark-bharat

# 2. Create virtual environment with Python 3.11
uv venv --python 3.11
source .venv/bin/activate

# 3. Install dependencies in editable mode
uv pip install -e ".[dev]"

# 4. Launch the Minimalist Sentinel Interface
uv run streamlit run app.py
```

---

## 🛡️ SEBI Hackathon Compliance Guarantee

- **0% Stock Tips / 0% Speculative Predictions:** Mathematically constrained at the schema layer from providing trading recommendations, price forecasts, or broker endorsements.
- **Statutory Precision:** Formulated in strict alignment with SEBI (Research Analysts) Regulations 2014, SEBI Performance Validation Agency (PVA) guidelines, and IT Act Section 66D.
