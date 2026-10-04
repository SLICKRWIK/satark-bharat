# SatarkBharat — Statutory Guardrails & Invariant Rules (`guardrails.md`)

> **Governing Standards:** SEBI Act 1992, SEBI (Research Analysts) Regulations 2014, SEBI (Investment Advisers) Regulations 2013, SEBI Master Circular on Intermediary Conduct, Information Technology Act 2000 (Section 66D).

---

## 1. Statutory Invariants & Legal Citations

### 1.1 Prohibition of Guaranteed Returns
- **Statute:** Regulation 15(1) & Schedule III of SEBI (Research Analysts) Regulations, 2014; SEBI Master Circular on Performance Claims by Intermediaries.
- **Rule:** No intermediary or entity may promise, guarantee, or indicate assured returns on investments or securities transactions.
- **Satark Penalty:** $+35$ Threat Score points. Instant high risk.

### 1.2 Mandatory Payment Segregation & Clearing Routing
- **Statute:** SEBI Circular `SEBI/HO/MIRSD/MIRSD-PoD-1/P/CIR/2023/71` and NPCI Directives on Broker Payment Gateways.
- **Rule:** All trading deposits and official advisory fees must be collected through registered corporate bank accounts / corporate merchant VPAs or direct clearing corporation settlement pools. Solicitation to personal UPI handles (`@paytm`, `@ybl`, `@okhdfcbank`, `@ibl`) is unauthorized.
- **Satark Penalty:** $+25$ Threat Score points.

### 1.3 Mandatory SEBI Registration for Advisory
- **Statute:** Section 12(1) of the SEBI Act, 1992.
- **Rule:** No person shall act as a stockbroker, merchant banker, portfolio manager, investment adviser, or research analyst without a certificate of registration granted by SEBI.
- **Satark Penalty:** $+30$ Threat Score points if missing; $+40$ if spoofing a legitimate entity.

### 1.4 Impersonation & Cyber Deceit
- **Statute:** Section 66D of the Information Technology Act, 2000 (Cheating by personation by using computer resource) & Bharatiya Nyaya Sanhita (BNS) Section 318(4) / IPC 420.
- **Rule:** Impersonating licensed market entities, forging SEBI seals, or distributing cloned APKs (`zer0dha.apk`) constitutes criminal cyber fraud.
- **Satark Action:** Auto-routes evidence to **National Cyber Crime Reporting Portal (NCRP / cybercrime.gov.in / Helpline 1930)** and **SEBI Market Intelligence (MI)**.

---

## 2. Hard Anti-Speculation Invariant (Hackathon Mandate)

```python
FORBIDDEN_INTENTS = [
    "STOCK_RECOMMENDATION",
    "TARGET_PRICE_PREDICTION",
    "BUY_SELL_CALL",
    "PORTFOLIO_ALLOCATION_ADVICE",
    "BROKER_PROMOTION"
]
```

Under no condition will SatarkBharat recommend or analyze individual stocks as investment vehicles. It functions exclusively as a **regulatory defense and threat intelligence sentinel**.
