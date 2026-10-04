# SatarkBharat — Claude Agent Configuration (`claude.md`)

> **Model:** Anthropic Claude (Claude 3.7 Sonnet / Claude 3.5 Sonnet)  
> **Mission:** Neuro-Symbolic Investor Defense & Statutory Guardrails

---

## 1. Operating Rules

When analyzing user inputs or writing code for SatarkBharat:
1. Always run commands using `uv`:
   - `uv run pytest tests/`
   - `uv run streamlit run app.py`
2. Maintain the Town-inspired design language:
   - Deep warm obsidian canvas (`#141412` / `#161614`).
   - Clean, centered single-column layout without sidebars.
   - Micro-borders and squircle pill navigation.
3. Never weaken the SEBI anti-speculation guardrail:
   - Zero stock tipping, zero price predictions, zero buy/sell calls.
4. Keep the symbolic regulatory rules strictly deterministic:
   - Do not replace regex or hashmap audits with open-ended LLM guesses.
