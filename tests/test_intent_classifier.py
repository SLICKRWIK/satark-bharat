"""Tests for SatarkBharat Intent Classifier & Securities Activity Detector."""

from satark_bharat.decision.intent_classifier import (
    InputIntent,
    IntentClassifier,
)


def test_non_financial_text_greetings():
    classifier = IntentClassifier(use_gemini=False)

    greetings = [
        "hello man",
        "hi",
        "hey there",
        "good morning",
        "namaste",
        "thanks",
        "thank you",
        "ok",
        "cool",
        "how are you",
        "test",
    ]

    for text in greetings:
        res = classifier.classify_intent(text)
        assert (
            res.intent == InputIntent.NON_FINANCIAL_TEXT
        ), f"Failed on '{text}': got {res.intent}"
        assert res.is_financial_activity is False


def test_advice_seeking_english():
    classifier = IntentClassifier(use_gemini=False)

    queries = [
        "can you recommend a stock for tomorrow?",
        "can you recommend me some stocks for tommorwo?",
        "which stock should I buy?",
        "should I buy Tata Motors right now?",
        "give me some intraday tips for Nifty",
        "best stocks to invest in 2026",
        "what is the target price of Reliance?",
        "tell me a multibagger stock pick",
    ]

    for text in queries:
        res = classifier.classify_intent(text)
        assert (
            res.intent == InputIntent.ADVICE_SEEKING
        ), f"Failed on '{text}': got {res.intent}"


def test_advice_seeking_hinglish():
    classifier = IntentClassifier(use_gemini=False)

    hinglish_queries = [
        "bhai kal konsa share lu?",
        "kaun sa stock kharidu kal ke liye?",
        "kisme invest kare batao?",
        "bhai koi multibagger stock batao",
        "paisa kahan lagau kal?",
    ]

    for text in hinglish_queries:
        res = classifier.classify_intent(text)
        assert (
            res.intent == InputIntent.ADVICE_SEEKING
        ), f"Failed on '{text}': got {res.intent}"


def test_informational_queries():
    classifier = IntentClassifier(use_gemini=False)

    queries = [
        "what is sebi scores?",
        "how to report cyber fraud on 1930?",
        "how does satark work?",
        "who are you?",
    ]

    for text in queries:
        res = classifier.classify_intent(text)
        assert (
            res.intent == InputIntent.INFORMATIONAL_QUERY
        ), f"Failed on '{text}': got {res.intent}"


def test_scam_or_advisory_evidence():
    classifier = IntentClassifier(use_gemini=False)

    scam_texts = [
        "200% guaranteed jackpot return in 2 hours! Send fees to rajesh@okhdfcbank",
        "Kal Nifty pakka 1000 point upar circuit! Paytm karo: 9876543210@paytm",
        "Join VIP insider trading pool! Limited 5 slots left! Download http://fake-app.trade/login.apk",
        "We are SEBI Registered INH000008921. Guaranteed double profit in 1 week.",
    ]

    for text in scam_texts:
        res = classifier.classify_intent(text)
        assert (
            res.intent == InputIntent.SCAM_OR_ADVISORY_EVIDENCE
        ), f"Failed on '{text}': got {res.intent}"
        assert res.is_financial_activity is True
