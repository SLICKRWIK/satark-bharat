"""Tests for SatarkBharat Telegram Bot Sentinel."""

import asyncio
from unittest.mock import AsyncMock, MagicMock

from satark_bharat.decision.threat_engine import ThreatIndexEngine
from satark_bharat.redressal.dossier import DossierGenerator
from satark_bharat.telegram_bot import (
    SatarkTelegramBot,
    extract_forward_provenance,
    format_threat_message,
)


def test_provenance_extraction_channel():
    mock_origin = MagicMock()
    mock_origin.type = "channel"
    mock_origin.chat = MagicMock(title="Nifty Wealth Secrets", username="niftysecrets")
    mock_origin.message_id = 452

    msg = MagicMock()
    msg.forward_origin = mock_origin
    provenance = extract_forward_provenance(msg)
    assert provenance == "Telegram Channel: Nifty Wealth Secrets (@niftysecrets) [Post #452]"


def test_provenance_extraction_direct_message():
    msg = MagicMock()
    msg.forward_origin = None
    msg.forward_from_chat = None
    msg.forward_from = None
    provenance = extract_forward_provenance(msg)
    assert provenance is None


def test_format_threat_message():
    engine = ThreatIndexEngine()
    report = engine.evaluate(
        "Pakka 200% guaranteed jackpot return! Send Rs 5000 to rajesh.kumar@okhdfcbank"
    )
    dossier_data = DossierGenerator.generate_json_dossier(report, "test raw evidence")
    sms_text = DossierGenerator.generate_1930_sms(report, dossier_data["incident_id"])

    formatted = format_threat_message(
        report=report,
        dossier_data=dossier_data,
        sms_text=sms_text,
        provenance="Telegram Channel: FakeVIP (@fakevip) [Post #101]",
        media_label="Forwarded Channel Message",
    )

    assert "SATARK BHARAT" in formatted
    assert "CRITICAL FRAUD ALERT" in formatted
    assert "100/100" in formatted
    assert "FakeVIP" in formatted
    assert "1930" in formatted
    assert "हिन्दी" in formatted


def test_sebi_anti_speculation_guardrail_refusal():
    bot = SatarkTelegramBot(token="123456:FAKE_TOKEN_FOR_TESTING")

    update = MagicMock()
    update.message = MagicMock()
    update.message.text = "Which stock should I buy for tomorrow's intraday profit?"
    update.message.reply_text = AsyncMock()
    update.message.forward_origin = None

    context = MagicMock()

    asyncio.run(bot.handle_text(update, context))

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args[0][0]
    assert "SEBI COMPLIANCE GUARDRAIL ENFORCED" in call_args
    assert "धोखाधड़ी निवारण प्रणाली" in call_args


def test_text_scam_message_handling():
    bot = SatarkTelegramBot(token="123456:FAKE_TOKEN_FOR_TESTING")

    update = MagicMock()
    update.message = MagicMock()
    update.message.text = (
        "EXCLUSIVE EXPIRY JACKPOT! 200% GUARANTEED RETURN in 2 Hours! "
        "Pay immediately to personal UPI: rajesh.advisory99@okhdfcbank"
    )
    update.message.forward_origin = None
    update.message.reply_text = AsyncMock()
    update.message.reply_document = AsyncMock()

    context = MagicMock()

    asyncio.run(bot.handle_text(update, context))

    # Assert structured text alert sent
    update.message.reply_text.assert_called_once()
    reply_text = update.message.reply_text.call_args[0][0]
    assert "CRITICAL FRAUD ALERT" in reply_text
    assert "100/100" in reply_text

    # Assert PDF document attached
    update.message.reply_document.assert_called_once()
    doc_call_kwargs = update.message.reply_document.call_args[1]
    assert "filename" in doc_call_kwargs
    assert doc_call_kwargs["filename"].startswith("Complaint_Dossier_SB-")
    assert doc_call_kwargs["filename"].endswith(".pdf")


def test_apk_document_handling():
    bot = SatarkTelegramBot(token="123456:FAKE_TOKEN_FOR_TESTING")

    doc_mock = MagicMock()
    doc_mock.file_name = "SuperNiftyPro_Trading_v3.apk"
    doc_mock.file_size = 15420300
    doc_mock.mime_type = "application/vnd.android.package-archive"

    update = MagicMock()
    update.message = MagicMock()
    update.message.document = doc_mock
    update.message.forward_origin = None
    update.message.reply_text = AsyncMock()
    update.message.reply_document = AsyncMock()

    context = MagicMock()

    asyncio.run(bot.handle_document(update, context))

    update.message.reply_text.assert_called_once()
    reply_text = update.message.reply_text.call_args[0][0]
    assert "CRITICAL FRAUD ALERT" in reply_text
    assert "Dangerous Android Application Package" in reply_text


def test_hello_man_zero_penalty_no_pdf():
    bot = SatarkTelegramBot(token="123456:FAKE_TOKEN_FOR_TESTING")

    update = MagicMock()
    update.message = MagicMock()
    update.message.text = "hello man"
    update.message.forward_origin = None
    update.message.reply_text = AsyncMock()
    update.message.reply_document = AsyncMock()

    context = MagicMock()

    asyncio.run(bot.handle_text(update, context))

    # Assert structured text alert sent
    update.message.reply_text.assert_called_once()
    reply_text = update.message.reply_text.call_args[0][0]
    assert "VERIFIED / LOW RISK" in reply_text
    assert "0/100" in reply_text
    assert "No statutory violations detected" in reply_text

    # Assert PDF document was NOT sent for 0 score
    update.message.reply_document.assert_not_called()
