"""SEBI Hackathon Compliance Guardrail: Deterministic Block on Stock Tipping & Speculation."""

import re
from dataclasses import dataclass


@dataclass
class GuardrailCheckResult:
    is_speculation_query: bool
    blocked_intent: str | None
    rejection_message_hindi: str
    rejection_message_english: str


class SebiComplianceGuardrail:
    # Heuristic expressions for queries asking for stock tips, predictions, or buy/sell calls
    SPECULATION_PATTERNS = [
        (re.compile(r"\b(which|what)\s+stock\b", re.IGNORECASE), "STOCK_PICKING_REQUEST"),
        (re.compile(r"\b(should\s+i\s+buy|should\s+i\s+sell|best\s+stock\s+to\s+buy)\b", re.IGNORECASE), "BUY_SELL_RECOMMENDATION"),
        (re.compile(r"\b(target\s+price|price\s+prediction|kal\s+kya\s+hoga|multibagger)\b", re.IGNORECASE), "PRICE_SPECULATION"),
        (re.compile(r"\b(portfolio\s+review|rebalance\s+my\s+portfolio)\b", re.IGNORECASE), "PORTFOLIO_ADVISORY_REQUEST"),
    ]

    def check_query(self, user_query: str) -> GuardrailCheckResult:
        query_clean = user_query.strip()
        for pattern, intent in self.SPECULATION_PATTERNS:
            if pattern.search(query_clean):
                return GuardrailCheckResult(
                    is_speculation_query=True,
                    blocked_intent=intent,
                    rejection_message_hindi="सतर्क भारत एक विनियामक सुरक्षा एवं धोखाधड़ी निवारण प्रणाली है। SEBI नियमों के अनुसार हम किसी भी शेयर या फंड की सिफारिश या भविष्यवाणी नहीं करते।",
                    rejection_message_english="SatarkBharat operates strictly as an investor defense sentinel. Under SEBI regulations, generative stock recommendations, price targets, and trading tips are strictly prohibited.",
                )

        return GuardrailCheckResult(
            is_speculation_query=False,
            blocked_intent=None,
            rejection_message_hindi="",
            rejection_message_english="",
        )
