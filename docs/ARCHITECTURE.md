# SatarkBharat — System Architecture & Data Flow

```mermaid
flowchart TD
    subgraph Client ["Client Interface (Town-Inspired Minimalist Web UI)"]
        UI_Input["Multimodal Ingestion Input (Text / OCR / Audio)"]
        UI_Chips["One-Click Scenario Chips (Case A / B / C / D)"]
        UI_Player["Vernacular Voice Warning Player (Hindi / Bengali / English)"]
        UI_Export["Court-Ready PDF Dossier & 1930 Cyber Cell SMS"]
    end

    subgraph Symbolic ["Deterministic Symbolic Regulatory Matrix"]
        REG_SEBI["SEBI Registry Auditor\n(Regex AST + Offline Intermediary Hashmap)"]
        REG_PAY["Payment Channel Auditor\n(Personal VPA vs Clearing Pool Invariant)"]
        REG_DOM["Domain Typosquatting Auditor\n(Levenshtein Distance + dnstwist Permutations)"]
        REG_PVA["Psychological & PVA Invariant Auditor\n(Guaranteed Returns & Syndicate Pooling Check)"]
    end

    subgraph Decision ["Decision & Guardrail Engine"]
        ENG_THREAT["Threat Index Engine\n(Mathematical Penalty Formula 0-100)"]
        ENG_GUARD["SEBI Compliance Guardrail\n(Mathematical Block on Stock Tipping)"]
        ENG_ROUTE["Jurisdictional Redressal Router\n(SCORES 2.0 vs NCRP 1930 / SEBI MI)"]
    end

    subgraph Redressal ["Evidentiary Packaging"]
        DOC_JSON["Structured Incident JSON"]
        DOC_PDF["Court-Ready PDF Docket (ReportLab)"]
        DOC_SMS["1930 Cyber Fraud Quick-Dial SMS"]
    end

    UI_Input --> REG_SEBI & REG_PAY & REG_DOM & REG_PVA
    UI_Chips --> UI_Input
    REG_SEBI & REG_PAY & REG_DOM & REG_PVA --> ENG_THREAT
    ENG_THREAT --> ENG_ROUTE
    ENG_ROUTE --> Redressal
    ENG_THREAT --> UI_Player
    Redressal --> UI_Export
```

---

## Component Descriptions

1. **`satark_bharat.symbolic.sebi_registry`**: Deterministic verification of alphanumeric SEBI codes (`INH`, `INA`, `INZ`, `INM`, `INP`, `MF`). Validates existence against `sebi_registry_snapshot.json` and detects entity spoofing.
2. **`satark_bharat.symbolic.payment_auditor`**: Enforces SEBI Circular `SEBI/HO/MIRSD/MIRSD-PoD-1/P/CIR/2023/71`. Flags consumer PSP handles (`@okhdfcbank`, `@paytm`, `@ybl`) solicited for fees.
3. **`satark_bharat.symbolic.domain_auditor`**: Scans for unauthorized APK downloads (`.apk`) and detects deceptive homoglyphs/typosquatting against verified benchmark domains (`zerodha.com`, `groww.in`, `sebi.gov.in`, `nseindia.com`).
4. **`satark_bharat.decision.threat_engine`**: Implements the mathematical penalty formula $T = \min\left(100, \sum W_i \cdot P_i\right)$ with instant red-line overrides.
5. **`satark_bharat.decision.guardrails`**: Enforces hard anti-speculation filters blocking stock tipping, price targets, or portfolio allocation advice.
6. **`satark_bharat.redressal.router`**: Top 1% differentiator bifurcating complaints between **SEBI SCORES 2.0** (registered entity impersonation) vs. **NCRP 1930 & SEBI MI** (unregistered criminal syndicate / cyber fraud).
7. **`satark_bharat.redressal.dossier`**: Compiles cryptographic SHA-256 evidence digests into court-ready PDF complaint packages and formatted 1930 Cyber Fraud helpline SMS dispatches.
