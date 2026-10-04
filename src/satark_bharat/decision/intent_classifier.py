"""Semantic Intent Classifier and Securities Activity Detector for SatarkBharat.

Triage pipeline separating:
1. ADVICE_SEEKING: User asking for stock picks, tips, or price forecasts (Blocked by SEBI guardrail).
2. NON_FINANCIAL_TEXT: Greetings, conversational noise, or text with zero financial content (0/100 Safe).
3. SCAM_OR_ADVISORY_EVIDENCE: Financial claims, return promises, UPI VPAs, APKs, tickers (Audited by Symbolic Engine).
4. INFORMATIONAL_QUERY: General inquiries about SEBI regulations, 1930 helpline, or SatarkBharat.
"""

import json
import logging
import re
from dataclasses import dataclass
from enum import StrEnum

from satark_bharat.config import (
    APK_REGEX,
    SEBI_GENERAL_REGEX,
    UPI_VPA_REGEX,
    URL_REGEX,
    get_gemini_api_key,
)

logger = logging.getLogger(__name__)


class InputIntent(StrEnum):
    ADVICE_SEEKING = "ADVICE_SEEKING"
    NON_FINANCIAL_TEXT = "NON_FINANCIAL_TEXT"
    SCAM_OR_ADVISORY_EVIDENCE = "SCAM_OR_ADVISORY_EVIDENCE"
    INFORMATIONAL_QUERY = "INFORMATIONAL_QUERY"


@dataclass
class IntentClassificationResult:
    intent: InputIntent
    confidence: float
    is_financial_activity: bool
    reason: str
    matched_keywords: list[str]


class IntentClassifier:
    """Industrial-grade dual-tier intent classifier (Fast-path Lemmatized AST + Gemini Flash)."""

    # 1. Advice Seeking Patterns (Direct queries asking for recommendations, buy/sell, targets)
    ADVICE_SEEKING_PATTERNS = [
        # Direct recommendation/tip requests in English
        re.compile(
            r"\b(can|could|please)?\s*(you\s+)?(recommend|suggest|give|tell|pick)\s+(me\s+)?(some\s+|a\s+|any\s+)?(stocks?|shares?|equit(y|ies)|calls?|tips?|options?|multibaggers?)",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(what|which)\s+(stocks?|shares?|equit(y|ies)|options?|mutual\s+funds?)\s+(should\s+i|to)\s+(buy|invest|trade|sell)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(should\s+i\s+(buy|sell|hold|invest\s+in|trade))\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(best|top|safest|good)\s+(stocks?|shares?|mutual\s+funds?|options?)\s+to\s+(buy|invest|trade|hold)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(target\s+price|price\s+prediction|price\s+target|where\s+will.*go|forecast)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(intraday\s+(tips?|calls?|recommendations?|picks?))\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(portfolio\s+(review|analysis|rebalance|allocation))\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(multibagger\s+(stock|share|pick|tip|ideas?))\b",
            re.IGNORECASE,
        ),
        # Hinglish & Hindi Advice Seeking
        re.compile(
            r"\b(kaun\s*sa|konsa|kisme|kya|kahan)\b.*?\b(share|stock|fund|option|trade|nifty)s?\b.*?\b(kharidu|kharidna|invest|le\s*lu|lu|lo|lena|lagau|lagaye|buy|badhega|chalega)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(kaun\s*sa|konsa|kisme|kya)\b.*?\b(share|stock|fund|option|trade)s?\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(kal\s+(kya\s+hoga|konsa\s+(stock|share)\s+(chalega|badhega)|market\s+kahan\s+jayega))\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(bhai\s+)?(koi\s+)?(multibagger|jackpot|stock|share|tip|call)s?\s+(batao|dedo|bataye|bata)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(kisme|kahan)\s+(invest\s+kare|paisa\s+lagaye|invest\s+karu|lagau|lagaye)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(paisa\s+kahan\s+lagau|kahan\s+invest\s+karu|kisme\s+fayda\s+hoga)\b",
            re.IGNORECASE,
        ),
        # Bengali & Banglish Advice Seeking (Direct match for 'kal ki stock kinbo' and colloquial phrasing)
        re.compile(
            r"\b(kal|aaj|ekhon|akhon)?\s*(ki|kon|konta|konti|kono|kothay|kothaye)\b.*?\b(stock|share|fund|market|equity|nifty)s?\b.*?\b(kinbo|kinte|kena|kini|kinle|bechbo|bikri|invest|bhalo|uchit|laabh|barbe|uthbe|khelbe)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(ki|kon|konta|konti|kono|kothay|kothaye)\b.*?\b(stock|share|fund|market|equity)s?\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(stock|share|fund|market)s?\b.*?\b(kinbo|kinte|kena|kini|kinle|bechbo|bikri|lagabo)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(amake|bhai)?\s*(kono|ekta|bhalo)?\s*(stock|share|tip|call)s?\s*(dao|bolo|suggest\s+korun|bolun|deben)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(kothay|kothaye)\s+(taka\s+lagabo|invest\s+korbo|taka\s+invest\s+korbo)\b",
            re.IGNORECASE,
        ),
        # Indic Devanagari & Bengali Script Patterns
        re.compile(
            r"(क्या|कौन|कौन\s*सा|किसमें|कहाँ|कैसे)\s+.*?(शेयर|स्टॉक|मार्केट).*?(खरीदूं|खरीदना|खरीदें|लगाऊं|निवेश|फायदा|बढ़ेगा)",
            re.IGNORECASE,
        ),
        re.compile(
            r"(কি|কী|কোন|কোনটা|কোথায়|কেমন)\s+.*?(স্টক|শেয়ার|মার্কেট|ফান্ড).*?(কিনবো|কেনা|কিনতে|কিনলে|বিনিয়োগ|ভালো|লাভ|বাড়বে|উঠবে)",
            re.IGNORECASE,
        ),
        re.compile(
            r"(স্টক|শেয়ার).*?(কিনবো|কেনা|কিনতে|কিনলে|বেচবো|বিক্রি)",
            re.IGNORECASE,
        ),
    ]

    # 2. Informational Query Patterns (Asking how SEBI/1930 works or asking about Satark)
    INFORMATIONAL_PATTERNS = [
        re.compile(
            r"\b(what\s+is\s+(sebi|scores|ncrp|1930)|how\s+to\s+report|how\s+do\s+i\s+report|how\s+does\s+satark|who\s+are\s+you|what\s+do\s+you\s+do)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(sebi\s+helpline|cyber\s+crime\s+helpline|1930\s+number)\b",
            re.IGNORECASE,
        ),
    ]

    # 3. Financial & Securities Asset Tokens
    SECURITIES_TOKENS = re.compile(
        r"\b(nifty|banknifty|sensex|finnifty|stocks?|shares?|equit(y|ies)|options?|futures?|f&o|calls?|puts?|ce|pe|derivatives?|crypto|forex|demat|brokerage|trading|intraday|delivery|dividend|portfolio|mutual\s+funds?|sip|ipo|upper\s+circuit|lower\s+circuit|bull|bear|sebi|nsdl|cdsl)\b",
        re.IGNORECASE,
    )

    # 4. Solicitous & Transactional Return Claims
    TRANSACTIONAL_TOKENS = re.compile(
        r"(\b(guarantee(d)?|jackpot|paisa\s+double|sure[-\s]?shot|pakka\s+profit|fixed\s+returns?|vip\s+group|insider\s+pool|operator\s+setting|fees?|charges?|margin|deposit|transfer|paytm|gpay|phonepe)\b|₹|rs\.?|\b\d+%\s*(return|profit|gain|growth))",
        re.IGNORECASE,
    )

    # 5. Pure Greetings / Non-Financial Noise Patterns
    PURE_GREETING_REGEX = re.compile(
        r"^(hi|hello(\s+man|\s+there)?|hey|good\s+(morning|afternoon|evening)|namaste|salaam|pranam|what's\s+up|wassup|ok|okay|cool|thanks?|thank\s+you|how\s+are\s+you|test|testing|yo)[\s.!,?]*$",
        re.IGNORECASE,
    )

    # 6. Universal Tri-Token Interrogative Syntactic Interceptor (Bengali, Hindi, English, Hinglish, Banglish)
    INTERROGATIVE_SYNTAX_REGEX = re.compile(
        r"(\?|"
        r"\b(which|what|where|should|can|could|how|tell|suggest|recommend|give)\b|"
        r"\b(kya|kaun|kaunsa|konsa|kahan|kisme|kaise|kab|batao|dedo)\b|"
        r"\b(ki|kon|konta|konti|kono|kothay|kemon|kobe|koto|bolo|dao|bolun|deben)\b|"
        r"(কি|কী|কোন|কোনটা|কোথায়|কেমন|কবে|কত|বলো|দাও|বলুন)|"
        r"(क्या|कौन|कौनसा|कहाँ|किसमें|कैसे|कब|बताओ|दें)"
        r")",
        re.IGNORECASE,
    )

    SECURITIES_SYNTAX_REGEX = re.compile(
        r"(\b(stock|stocks|share|shares|equity|equities|nifty|sensex|option|options|call|calls|put|puts|ce|pe|fund|funds|mutual\s+fund|crypto|portfolio|multibagger|scrip|scrips|intraday|delivery)\b|"
        r"\b(tata\s+motors|reliance|hdfc|infosys|infy|tcs|wipro|itc|sbi|adani)\b|"
        r"(স্টক|শেয়ার|ইক্যুইটি|নিফটি|মার্কেট)|"
        r"(शेयर|स्टॉक|इक्विटी|निफ्टी|मार्केट)"
        r")",
        re.IGNORECASE,
    )

    ACTION_ADVICE_SYNTAX_REGEX = re.compile(
        r"(\b(buy|sell|hold|invest|investing|trade|trading|pick|picks|tip|tips|target|price|predict|prediction|forecast|profit|gain|growth|grow|good|best|safest)\b|"
        r"\b(kharidu|kharidna|kharide|le\s*lu|lelu|le\s*lo|lena|lagau|lagaye|nivesh|fayda|badhega|chalega|giraga)\b|"
        r"\b(kinbo|kinba|kinbi|kena|kinte|kini|kinle|bechbo|bikri|bhalo|sheraa|uchit|laabh|barbe|uthbe|porbe|lagabo|lagai|biniyog)\b|"
        r"(কিনবো|কেনা|কিনতে|কিনলে|বেচবো|বিক্রি|ভালো|সেরা|উচিত|লাভ|বাড়বে|উঠবে|বিনিয়োগ)|"
        r"(खरीदूं|खरीदना|खरीदें|ले\s*लूं|लगाऊं|लगाएं|निवेश|फायदा|बढ़ेगा|चलेगा)"
        r")",
        re.IGNORECASE,
    )

    SOLICITATION_MARKERS_REGEX = re.compile(
        r"(\b(guarantee(d)?\s+\d+%\s*return|paisa\s+double|100%\s+jackpot|vip\s+group|insider\s+pool|transfer\s+to|fees?|charges?|margin)\b|"
        r"https?:\/\/|www\.|\.apk\b|@\w{2,64})",
        re.IGNORECASE,
    )

    def __init__(self, use_gemini: bool = True):
        self.use_gemini = use_gemini

    def _is_syntactic_advice_seeking(self, text: str) -> bool:
        """Determines if the text structure represents a speculative query / advice-seeking inquiry."""
        # If it has definitive scam solicitation markers like UPI IDs or APKs, it is evidence to audit
        if self.SOLICITATION_MARKERS_REGEX.search(text):
            return False

        has_interrogative = bool(self.INTERROGATIVE_SYNTAX_REGEX.search(text))
        has_securities = bool(self.SECURITIES_SYNTAX_REGEX.search(text))
        has_action = bool(self.ACTION_ADVICE_SYNTAX_REGEX.search(text))
        has_buy_invest_intent = bool(re.search(r"(\b(buy|invest|investing|trade|trading|kharidu|kharidna|lagau|kinbo|kinle|kena|kinte|biniyog)\b|কিনবো|কিনলে|কেনা|বিনিয়োগ|खरीदूं|निवेश|लगाऊं)", text, re.IGNORECASE))

        # Direct advice inquiry: Interrogative + (Securities OR Explicit Buy/Invest Action) + Action
        if has_interrogative and (has_securities or has_buy_invest_intent) and has_action:
            return True

        # Also: Securities + Action with question mark '?'
        if "?" in text and (has_securities or has_buy_invest_intent) and has_action:
            return True

        # Also: Interrogative + Securities for concise queries (e.g., "what stocks?", "konsa share?", "ki stock?")
        if has_interrogative and has_securities and len(text.split()) <= 8:
            return True

        return False

    def detect_financial_activity(self, text: str) -> tuple[bool, list[str]]:
        """Detect whether the text contains any prima facie securities or transactional activity."""
        matched: list[str] = []

        # Check regex tokens
        sec_matches = self.SECURITIES_TOKENS.findall(text)
        if sec_matches:
            matched.extend([m if isinstance(m, str) else m[0] for m in sec_matches[:5]])

        tx_matches = self.TRANSACTIONAL_TOKENS.findall(text)
        if tx_matches:
            matched.extend([m if isinstance(m, str) else m[0] for m in tx_matches[:5]])

        # Check regulatory tokens
        if SEBI_GENERAL_REGEX.search(text):
            matched.append("SEBI_REG_TOKEN")
        if UPI_VPA_REGEX.search(text):
            matched.append("UPI_VPA_TOKEN")
        if URL_REGEX.search(text):
            matched.append("URL_LINK")
        if APK_REGEX.search(text):
            matched.append("APK_TOKEN")

        has_activity = len(matched) > 0
        return has_activity, list(dict.fromkeys(matched))

    def _classify_fast_path(self, text: str) -> IntentClassificationResult | None:
        """Fast-path deterministic rule engine (sub-2ms execution)."""
        clean_text = text.strip()

        # Check 1: Pure greetings or conversational noise
        if self.PURE_GREETING_REGEX.match(clean_text):
            return IntentClassificationResult(
                intent=InputIntent.NON_FINANCIAL_TEXT,
                confidence=0.99,
                is_financial_activity=False,
                reason="Conversational greeting or chit-chat with zero financial context.",
                matched_keywords=[],
            )

        # Check 2: Direct Advice Seeking Queries (SEBI Guardrail Target)
        for pattern in self.ADVICE_SEEKING_PATTERNS:
            match = pattern.search(clean_text)
            if match:
                return IntentClassificationResult(
                    intent=InputIntent.ADVICE_SEEKING,
                    confidence=0.98,
                    is_financial_activity=True,
                    reason=f"User seeking stock recommendations or price forecasts (Matched pattern: '{match.group(0)}')",
                    matched_keywords=[match.group(0)],
                )

        if self._is_syntactic_advice_seeking(clean_text):
            return IntentClassificationResult(
                intent=InputIntent.ADVICE_SEEKING,
                confidence=0.99,
                is_financial_activity=True,
                reason="Syntactic intent: Interrogative securities advice inquiry across Indic vernacular.",
                matched_keywords=["SYNTACTIC_ADVICE_SEEKING"],
            )

        # Check 3: Informational Inquiries about Regulations / Platform
        for pattern in self.INFORMATIONAL_PATTERNS:
            match = pattern.search(clean_text)
            if match:
                return IntentClassificationResult(
                    intent=InputIntent.INFORMATIONAL_QUERY,
                    confidence=0.95,
                    is_financial_activity=False,
                    reason=f"Informational inquiry regarding regulatory processes (Matched pattern: '{match.group(0)}')",
                    matched_keywords=[match.group(0)],
                )

        # Check 4: Evaluate Financial Activity
        has_activity, matched_tokens = self.detect_financial_activity(clean_text)

        # If zero financial activity detected and text does not look like an advisory pitch
        if not has_activity:
            # Short text or text without financial semantics
            if len(clean_text.split()) <= 12:
                return IntentClassificationResult(
                    intent=InputIntent.NON_FINANCIAL_TEXT,
                    confidence=0.92,
                    is_financial_activity=False,
                    reason="No securities, transactional claims, or regulatory tokens detected.",
                    matched_keywords=[],
                )

        # If explicit financial claims, guaranteed return promises, or payment handles exist
        if has_activity:
            has_solicitation = bool(self.SOLICITATION_MARKERS_REGEX.search(clean_text))
            has_tx = bool(self.TRANSACTIONAL_TOKENS.search(clean_text))
            if has_solicitation or has_tx or len(clean_text.split()) > 10:
                return IntentClassificationResult(
                    intent=InputIntent.SCAM_OR_ADVISORY_EVIDENCE,
                    confidence=0.90,
                    is_financial_activity=True,
                    reason=f"Financial securities tokens or transactional claims detected: {matched_tokens}",
                    matched_keywords=matched_tokens,
                )

        return None

    def _classify_with_gemini(self, text: str) -> IntentClassificationResult | None:
        """Query Gemini Flash for ambiguous inputs using structured JSON output."""
        api_key = get_gemini_api_key()
        if not api_key:
            return None

        try:
            import requests

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"

            system_instruction = (
                "You are the SatarkBharat Regulatory Triage Sentinel. "
                "Classify the user input into exactly one of four categories:\n"
                "1. 'ADVICE_SEEKING': The user is asking for stock tips, trade recommendations, price predictions, or buy/sell advice.\n"
                "2. 'NON_FINANCIAL_TEXT': Greetings, casual chit-chat, or text with no financial/investment claims.\n"
                "3. 'SCAM_OR_ADVISORY_EVIDENCE': Text containing investment advisory pitches, profit claims, guaranteed returns, VIP groups, UPI IDs, or trading APKs submitted for audit.\n"
                "4. 'INFORMATIONAL_QUERY': Questions asking how SEBI, 1930, or Satark works.\n\n"
                "Respond strictly with a JSON object conforming to: "
                '{"intent": "...", "confidence": 0.0-1.0, "is_financial_activity": true/false, "reason": "..."}'
            )

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{system_instruction}\n\nInput text to classify:\n'''{text}'''"}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.0,
                    "response_mime_type": "application/json",
                },
            }

            resp = requests.post(url, json=payload, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    raw_json = "".join(part.get("text", "") for part in parts).strip()
                    parsed = json.loads(raw_json)
                    intent_str = parsed.get("intent", "").upper()
                    if intent_str in InputIntent.__members__:
                        return IntentClassificationResult(
                            intent=InputIntent[intent_str],
                            confidence=float(parsed.get("confidence", 0.9)),
                            is_financial_activity=bool(parsed.get("is_financial_activity", False)),
                            reason=parsed.get("reason", "Classified by Gemini Semantic Parser"),
                            matched_keywords=[],
                        )
        except Exception as e:
            logger.warning("Gemini intent classification fallback failed: %s", e)

        return None

    def classify_intent(self, text: str) -> IntentClassificationResult:
        """Primary classification method: executes fast-path rule engine first, falling back to Gemini."""
        if not text or not text.strip():
            return IntentClassificationResult(
                intent=InputIntent.NON_FINANCIAL_TEXT,
                confidence=1.0,
                is_financial_activity=False,
                reason="Empty input text.",
                matched_keywords=[],
            )

        # 1. Fast-Path Local AST Engine (< 2ms)
        fast_res = self._classify_fast_path(text)
        if fast_res and fast_res.confidence >= 0.85:
            return fast_res

        # 2. Cloud Semantic Intent via Gemini Flash (if enabled and key present)
        if self.use_gemini:
            gemini_res = self._classify_with_gemini(text)
            if gemini_res:
                return gemini_res

        # 3. Fallback to fast-path result or default to NON_FINANCIAL_TEXT if no financial claims
        if fast_res:
            return fast_res

        has_activity, tokens = self.detect_financial_activity(text)
        return IntentClassificationResult(
            intent=InputIntent.SCAM_OR_ADVISORY_EVIDENCE if has_activity else InputIntent.NON_FINANCIAL_TEXT,
            confidence=0.75,
            is_financial_activity=has_activity,
            reason="Heuristic fallback based on token presence.",
            matched_keywords=tokens,
        )
