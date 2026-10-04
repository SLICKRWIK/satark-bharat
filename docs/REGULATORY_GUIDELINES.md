# SatarkBharat — Statutory & Regulatory Guidelines Compliance Manual

> **Reference Manual for IIT-BHU × SEBI × NSDL Hackathon Evaluation**  
> **Key Enforcement Bodies:** Securities and Exchange Board of India (SEBI), Indian Cyber Crime Coordination Centre (I4C), National Cyber Crime Reporting Portal (NCRP), Clearing Corporation of India (CCIL/NSCCL).

---

## 1. Statutory Invariants & SEBI Framework

### 1.1 Prohibition of Guaranteed Returns
- **Statutory Authority:** SEBI (Research Analysts) Regulations, 2014 — Regulation 15(1) & Schedule III (Code of Conduct); SEBI (Investment Advisers) Regulations, 2013 — Regulation 15(1); SEBI Master Circular on Intermediary Conduct.
- **Regulatory Doctrine:** No regulated entity (RA, IA, Broker, Portfolio Manager) is permitted to state, promise, or imply guaranteed, assured, or fixed returns on securities or derivatives transactions.
- **Enforcement Action:** Violations result in administrative debarment from capital markets, impounding of unlawful gains, and suspension of registration certificate.
- **SatarkBharat Auditing:** Analyzes text/speech for assurance tokens (`guaranteed`, `fixed profit`, `pakka return`, `100% loss-free`, `sure-shot jackpot`) and assigns $+35$ penalty points.

### 1.2 Mandatory Payment Segregation & Clearing Routing
- **Statutory Authority:** SEBI Circular `SEBI/HO/MIRSD/MIRSD-PoD-1/P/CIR/2023/71` and NPCI Directives on Broker Payment Channels.
- **Regulatory Doctrine:** Monies received for trading margins, brokerage, or authorized advisory fees cannot be deposited into personal savings bank accounts or individual consumer VPAs (`@okhdfcbank`, `@paytm`, `@ybl`, `@okaxis`). Fees must be remitted through corporate merchant gateways or clearing member settlement accounts.
- **Enforcement Action:** Immediate investigation for unauthorized fund diversion, tax evasion, and unregistered portfolio pooling.
- **SatarkBharat Auditing:** Extracts VPAs and inspects the PSP bank domain. Consumer PSP handles trigger an instant $+25$ penalty.

### 1.3 Mandatory Certificate of Registration
- **Statutory Authority:** Section 12(1) of the SEBI Act, 1992.
- **Regulatory Doctrine:** No person shall act as a stockbroker, merchant banker, portfolio manager, investment adviser, or research analyst without a certificate of registration granted by SEBI.
- **Enforcement Action:** Search, seizure, and criminal prosecution under Section 24 of the SEBI Act.
- **SatarkBharat Auditing:** Verifies alphanumeric prefixes (`INH`, `INA`, `INZ`, `INM`, `INP`, `MF`) against the offline registry snapshot.

---

## 2. Institutional Jurisdictional Routing (The Winning Moat)

A critical distinction understood by regulatory officers is that **different portals have mutually exclusive jurisdictions**:

```
                                [ Incident Analyzed ]
                                          │
            ┌─────────────────────────────┴─────────────────────────────┐
            ▼                                                           ▼
[ Respondent claims genuine SEBI ID ]                      [ Unregistered / Fake Syndicate ]
- Existing intermediary code                               - Fake alphanumeric or no ID
- Spoofing or intermediary misconduct                      - Telegram/WhatsApp pump-and-dump
            │                                                           │
            ▼                                                           ▼
  [ SEBI SCORES 2.0 Portal ]                                 [ NCRP 1930 + SEBI MI Portal ]
  • scores.sebi.gov.in                                       • cybercrime.gov.in / Dial 1930
  • Action: Formal intermediary grievance                     • Action: Immediate VPA/Bank freeze
  • Requires: Folio / Intermediary ID                        • Action: SEBI Market Intelligence raid
```

### 2.1 When to Route to SEBI SCORES 2.0
- **Condition:** The respondent is an authentic registered entity (or impersonating a registered entity code) and the claim involves authorized market intermediaries.
- **Limitation:** SCORES 2.0 rejects grievances filed against unknown/anonymous Telegram channels or individuals without a registered intermediary code.

### 2.2 When to Route to NCRP (cybercrime.gov.in / 1930) and SEBI Market Intelligence (MI)
- **Condition:** The perpetrator is operating an unregistered illegal pool, soliciting cash via personal UPI, distributing malicious APKs, or running social media syndicates.
- **Mandate:** Section 66D of the IT Act (Cheating by personation) and Section 318(4) Bharatiya Nyaya Sanhita (BNS) / IPC 420.
- **NCRP 1930 Golden Hour:** The 1930 national helpline enables victim banks and payment switches to freeze beneficiary accounts before illicit funds are laundered.

---

## 3. SEBI Hackathon Compliance Guardrail

To maintain 100% adherence to hackathon safety mandates:
1. **Zero Stock Tipping:** The system contains zero endpoints or prompts recommending equities, derivatives, mutual funds, or commodities.
2. **Zero Price Forecasting:** The system refuses all requests for target prices or expiry forecasts.
3. **Pure Defensive Sentinel:** The software operates solely as an analytical protective shield evaluating regulatory compliance and cyber risk.
