"""SatarkBharat Telegram Bot Sentinel.

Provides a real-time conversational and multimodal investor defense interface on Telegram.
Handles:
1. Forwarded messages from illicit Telegram trading channels (with origin channel attribution).
2. Direct advisory text messages and suspicious return promises.
3. Screenshots and payment QR/VPA images via Gemini Multimodal Vision / OCR.
4. Vernacular voice notes (.oga / .ogg / .mp3) via Gemini Speech.
5. Android APK attachments (immediate critical threat intercept).
6. SEBI Compliance Guardrails (refusing stock tipping / price speculation queries).
7. Auto-generated Court-Ready PDF Complaint Dossier delivery.
"""

import html
import io
import logging
from typing import Any

from telegram import Message, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from satark_bharat.config import get_gemini_api_key, get_telegram_bot_token
from satark_bharat.decision.guardrails import SebiComplianceGuardrail
from satark_bharat.decision.threat_engine import ThreatIndexEngine, ThreatReport
from satark_bharat.ingestion.audio import AudioIngestionModule
from satark_bharat.ingestion.ocr import VisualOcrIngestion
from satark_bharat.redressal.dossier import DossierGenerator

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("satark_telegram_bot")


def extract_forward_provenance(message: Message) -> str | None:
    """Extract provenance metadata from forwarded messages (channels, groups, users)."""
    if hasattr(message, "forward_origin") and message.forward_origin:
        origin = message.forward_origin
        origin_type = getattr(origin, "type", "")
        if origin_type == "channel":
            chat = getattr(origin, "chat", None)
            title = getattr(chat, "title", "Unknown Channel")
            username = getattr(chat, "username", None)
            uname_str = f" (@{username})" if username else ""
            msg_id = getattr(origin, "message_id", "")
            return f"Telegram Channel: {title}{uname_str} [Post #{msg_id}]"
        if origin_type == "chat":
            sender_chat = getattr(origin, "sender_chat", None)
            title = getattr(sender_chat, "title", "Group Chat")
            return f"Telegram Group: {title}"
        if origin_type == "user":
            user = getattr(origin, "sender_user", None)
            name = getattr(user, "full_name", "Telegram User")
            username = getattr(user, "username", None)
            uname_str = f" (@{username})" if username else ""
            return f"Telegram User: {name}{uname_str}"
        if origin_type == "hidden_user":
            name = getattr(origin, "sender_user_name", "Privacy-Protected Account")
            return f"Hidden Account: {name}"

    # Legacy or fallback attributes
    if getattr(message, "forward_from_chat", None):
        chat = message.forward_from_chat
        title = getattr(chat, "title", "Forwarded Chat")
        uname = getattr(chat, "username", None)
        uname_str = f" (@{uname})" if uname else ""
        return f"Chat: {title}{uname_str}"

    if getattr(message, "forward_from", None):
        user = message.forward_from
        name = getattr(user, "full_name", "Forwarded Sender")
        uname = getattr(user, "username", None)
        uname_str = f" (@{uname})" if uname else ""
        return f"Sender: {name}{uname_str}"

    return None


def format_threat_message(
    report: ThreatReport,
    dossier_data: dict[str, Any],
    sms_text: str,
    provenance: str | None = None,
    media_label: str | None = None,
) -> str:
    """Format a clean, structured HTML alert for Telegram users."""
    score = report.composite_threat_score
    severity = report.severity

    if score <= 24:
        status_icon = "🟢"
        headline = "VERIFIED / LOW RISK"
    elif score <= 59:
        status_icon = "🟡"
        headline = "MODERATE CAUTION REQUIRED"
    elif score <= 84:
        status_icon = "🟠"
        headline = "HIGH THREAT DETECTED"
    else:
        status_icon = "🚨"
        headline = "CRITICAL FRAUD ALERT"

    incident_id = dossier_data.get("incident_id", "SB-EVAL")
    target_portal = dossier_data.get("target_portal", {})
    portal_name = target_portal.get("name", "NCRP 1930 / SEBI")

    lines = [
        "🛡️ <b>SATARK BHARAT — INVESTOR DEFENSE SENTINEL</b>",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"<b>Verdict:</b> {status_icon} <b>{headline}</b>",
        f"<b>Threat Index:</b> <code>{score}/100</code> ({severity})",
    ]

    if media_label:
        lines.append(f"<b>Input Source:</b> <i>{html.escape(media_label)}</i>")

    if provenance:
        lines.append(f"📢 <b>Originating Source:</b> <code>{html.escape(provenance)}</code>")

    if report.red_line_triggered and report.red_line_reason:
        lines.append("")
        lines.append(f"⛔ <b>RED LINE TRIGGER:</b> {html.escape(report.red_line_reason)}")

    # Violations
    if report.statutory_violations:
        lines.append("")
        lines.append("⚖️ <b>Regulatory & Statutory Violations:</b>")
        for v in report.statutory_violations[:4]:
            lines.append(f"• {html.escape(v)}")

    # Vernacular summary
    lines.append("")
    lines.append("🗣️ <b>Investor Advisory:</b>")
    lines.append(f"🇮🇳 <b>हिन्दी:</b> {html.escape(report.vernacular_hindi_summary)}")
    lines.append(f"🇬🇧 <b>English:</b> {html.escape(report.plain_english_summary)}")

    # Redressal Routing
    lines.append("")
    lines.append("🏛️ <b>Recommended Redressal Route:</b>")
    lines.append(f"• <b>Authority:</b> {html.escape(portal_name)}")
    lines.append(f"• <b>Incident Docket:</b> <code>{html.escape(incident_id)}</code>")

    # 1930 Helpline dispatch snippet if elevated threat
    if score >= 60:
        lines.append("")
        lines.append("📞 <b>Helpline 1930 Quick Dispatch:</b>")
        lines.append(f"<pre>{html.escape(sms_text)}</pre>")
        lines.append("<i>(Tap text above to copy and submit to 1930 or cybercrime.gov.in)</i>")

    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    if score >= 25:
        lines.append("📎 <i>Official Court-Ready PDF Complaint Dossier attached below:</i>")
    else:
        lines.append("✅ <i>No statutory violations detected. No complaint filing required.</i>")

    return "\n".join(lines)


class SatarkTelegramBot:
    """Telegram Bot Controller wrapping the SatarkBharat neuro-symbolic engine."""

    def __init__(self, token: str | None = None):
        self.token = token or get_telegram_bot_token()
        if not self.token:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN not found in environment or .env file. "
                "Please configure TELEGRAM_BOT_TOKEN to launch the bot."
            )

        self.threat_engine = ThreatIndexEngine()
        self.ocr_engine = VisualOcrIngestion()
        self.audio_engine = AudioIngestionModule()
        self.guardrail = SebiComplianceGuardrail()

    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command with multilingual introduction and usage guidance."""
        if not update.message:
            return

        welcome_text = (
            "🙏 <b>Namaste! Welcome to SatarkBharat AI Sentinel</b>\n"
            "<i>Pre-Transaction Neuro-Symbolic Defense for Indian Retail Investors</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Protect yourself against fake SEBI advisers, illegal 'VIP jackpot' groups, "
            "unregistered operator pooling, and fraudulent trading apps.\n\n"
            "📲 <b>How to Use:</b>\n"
            "1️⃣ <b>Forward any message</b> from Telegram channels, groups, or chats.\n"
            "2️⃣ <b>Send a Screenshot</b> of chat promises, WhatsApp tips, or payment QR/VPAs.\n"
            "3️⃣ <b>Send a Voice Note</b> in Hindi, Bengali, Hinglish, or English.\n"
            "4️⃣ <b>Paste advisory text</b> or links directly here.\n\n"
            "⚡ <b>What SatarkBharat Provides:</b>\n"
            "• Instant 0–100 Threat Index\n"
            "• SEBI Registry & Impersonation verification\n"
            "• Personal UPI VPA & Typosquatted Domain check\n"
            "• 1930 Cyber Fraud SMS template\n"
            "• Court-Ready Complaint Dossier PDF attached immediately\n\n"
            "⚠️ <i>Mandatory Guardrail Notice: Under SEBI (Research Analysts) Regulations, "
            "SatarkBharat NEVER provides stock tips, price targets, or trading recommendations.</i>"
        )
        await update.message.reply_text(welcome_text, parse_mode=ParseMode.HTML)

    async def handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command."""
        if not update.message:
            return

        help_text = (
            "📖 <b>SatarkBharat Help & Emergency Guidelines</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🚨 <b>Emergency Cyber Crime Helpline:</b> Call <b>1930</b> immediately if you have transferred funds.\n"
            "🌐 <b>National Portal:</b> https://cybercrime.gov.in\n"
            "🏛️ <b>SEBI Investor Grievances:</b> https://scores.sebi.gov.in\n\n"
            "<b>Bot Commands:</b>\n"
            "/start - Show welcome instructions\n"
            "/help - Emergency assistance and commands\n"
            "/status - Verify engine status and SEBI registry database"
        )
        await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

    async def handle_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /status command to check system health."""
        if not update.message:
            return

        sebi_count = len(getattr(self.threat_engine.sebi_auditor, "registry", {}))
        domains_count = len(getattr(self.threat_engine.domain_auditor, "verified_domains", {}))
        gemini_ready = bool(get_gemini_api_key())

        status_text = (
            "⚙️ <b>SatarkBharat System Diagnostics</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• <b>SEBI Registry Auditor:</b> Active ({sebi_count} verified intermediaries)\n"
            f"• <b>Domain & Broker Auditor:</b> Active ({domains_count} verified broker domains)\n"
            f"• <b>NSDL Depository Auditor:</b> Active\n"
            f"• <b>Payment Channel Auditor:</b> Active (Personal VPA detection enabled)\n"
            f"• <b>Multimodal Vision & Audio (Gemini):</b> {'🟢 Connected' if gemini_ready else '🟡 Offline / Heuristic Mode'}\n"
            f"• <b>Engine Status:</b> 🟢 Ready for instant pre-transaction audit"
        )
        await update.message.reply_text(status_text, parse_mode=ParseMode.HTML)

    async def _audit_and_reply(
        self,
        update: Update,
        evidence_text: str,
        provenance: str | None = None,
        media_label: str | None = None,
    ) -> None:
        """Core pipeline: evaluates evidence, checks guardrails, replies with alert and attached PDF dossier."""
        if not update.message:
            return

        # Step 1: SEBI Anti-Speculation Guardrail
        guardrail_result = self.guardrail.check_query(evidence_text)
        if guardrail_result.is_speculation_query:
            rejection_msg = (
                "🛡️ <b>SEBI COMPLIANCE GUARDRAIL ENFORCED</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🇮🇳 <b>हिन्दी:</b> {html.escape(guardrail_result.rejection_message_hindi)}\n\n"
                f"🇬🇧 <b>English:</b> {html.escape(guardrail_result.rejection_message_english)}\n\n"
                "<i>SatarkBharat operates strictly as an investor defense and fraud prevention sentinel. "
                "Consult only SEBI-registered Research Analysts (INH) or Investment Advisers (INA).</i>"
            )
            await update.message.reply_text(rejection_msg, parse_mode=ParseMode.HTML)
            return

        # Prepend forward provenance into evidence text if available
        full_evidence = evidence_text
        if provenance:
            full_evidence = f"[PROVENANCE: {provenance}]\n\n{evidence_text}"

        # Step 2: Evaluate threat
        report = self.threat_engine.evaluate(full_evidence)

        # Step 3: Generate evidentiary dossier & 1930 dispatch
        dossier_data = DossierGenerator.generate_json_dossier(report, full_evidence)
        pdf_bytes = DossierGenerator.generate_pdf_dossier(dossier_data)
        sms_text = DossierGenerator.generate_1930_sms(report, dossier_data["incident_id"])

        # Step 4: Send structured alert text
        alert_msg = format_threat_message(
            report=report,
            dossier_data=dossier_data,
            sms_text=sms_text,
            provenance=provenance,
            media_label=media_label,
        )
        await update.message.reply_text(alert_msg, parse_mode=ParseMode.HTML)

        # Step 5: Send attached court-ready PDF complaint package only for elevated threat
        if report.composite_threat_score >= 25:
            try:
                pdf_stream = io.BytesIO(pdf_bytes)
                pdf_filename = f"Complaint_Dossier_{dossier_data['incident_id']}.pdf"
                pdf_stream.name = pdf_filename
                await update.message.reply_document(
                    document=pdf_stream,
                    filename=pdf_filename,
                    caption=f"📄 Evidentiary Complaint Dossier [{dossier_data['incident_id']}] for SEBI SCORES 2.0 / NCRP 1930",
                )
            except Exception as e:
                logger.error("Failed to send PDF document: %s", e)

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle incoming text messages and forwarded text messages."""
        if not update.message or not update.message.text:
            return

        text = update.message.text.strip()
        provenance = extract_forward_provenance(update.message)
        media_label = "Forwarded Channel Message" if provenance else "Direct Text Message"

        await self._audit_and_reply(
            update=update,
            evidence_text=text,
            provenance=provenance,
            media_label=media_label,
        )

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle screenshot and photo uploads via Gemini Multimodal Vision / OCR."""
        if not update.message or not update.message.photo:
            return

        status_msg = await update.message.reply_text(
            "🔍 <i>Analyzing screenshot with Satark Multimodal Vision...</i>",
            parse_mode=ParseMode.HTML,
        )

        try:
            # Download highest resolution photo
            photo = update.message.photo[-1]
            tg_file = await photo.get_file()
            file_bytes = await tg_file.download_as_bytearray()

            # Include caption text if user added one
            caption = update.message.caption or ""

            # Extract text using Gemini Vision or OCR fallback
            extracted_text = self.ocr_engine.extract_text_from_image(
                bytes(file_bytes), mime_type="image/jpeg"
            )

            combined_text = extracted_text
            if caption:
                combined_text = f"{caption}\n\n[SCREENSHOT OCR CONTENT]:\n{extracted_text}"

            provenance = extract_forward_provenance(update.message)
            media_label = "Screenshot / Image Upload"

            # Delete temporary analyzing message
            try:
                await status_msg.delete()
            except Exception:
                pass

            await self._audit_and_reply(
                update=update,
                evidence_text=combined_text,
                provenance=provenance,
                media_label=media_label,
            )
        except Exception as e:
            logger.error("Error processing photo: %s", e)
            await update.message.reply_text(
                f"❌ Failed to process screenshot: {e}",
                parse_mode=ParseMode.HTML,
            )

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle voice notes and audio clips (.oga / .ogg / .mp3) via Gemini Speech."""
        if not update.message:
            return

        audio_obj = update.message.voice or update.message.audio
        if not audio_obj:
            return

        status_msg = await update.message.reply_text(
            "🎧 <i>Transcribing vernacular audio note with Satark Speech Sentinel...</i>",
            parse_mode=ParseMode.HTML,
        )

        try:
            tg_file = await audio_obj.get_file()
            file_bytes = await tg_file.download_as_bytearray()

            # Determine filename
            filename = "voice_note.oga"
            if hasattr(audio_obj, "file_name") and audio_obj.file_name:
                filename = audio_obj.file_name

            # Transcribe with Gemini
            transcribed_text = self.audio_engine.transcribe_audio(
                bytes(file_bytes), filename=filename
            )

            provenance = extract_forward_provenance(update.message)
            media_label = f"Voice Note / Audio ({filename})"

            try:
                await status_msg.delete()
            except Exception:
                pass

            await self._audit_and_reply(
                update=update,
                evidence_text=transcribed_text,
                provenance=provenance,
                media_label=media_label,
            )
        except Exception as e:
            logger.error("Error processing audio: %s", e)
            await update.message.reply_text(
                f"❌ Failed to process voice note: {e}",
                parse_mode=ParseMode.HTML,
            )

    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle uploaded documents: APK files, images, or text files."""
        if not update.message or not update.message.document:
            return

        doc = update.message.document
        file_name = (doc.file_name or "").lower()
        mime_type = (doc.mime_type or "").lower()

        # Check for APK file upload
        if file_name.endswith(".apk") or "package-archive" in mime_type:
            apk_evidence = (
                f"UNOFFICIAL MALICIOUS APK FILE ATTACHED: {doc.file_name}\n"
                f"File Size: {doc.file_size} bytes\n"
                f"MIME: {doc.mime_type}\n"
                "Offense: Distribution of unverified malicious trading terminal application."
            )
            provenance = extract_forward_provenance(update.message)
            await self._audit_and_reply(
                update=update,
                evidence_text=apk_evidence,
                provenance=provenance,
                media_label=f"Dangerous Android Application Package ({doc.file_name})",
            )
            return

        # Check for uncompressed image document
        if mime_type.startswith("image/"):
            status_msg = await update.message.reply_text(
                "🔍 <i>Analyzing image document...</i>",
                parse_mode=ParseMode.HTML,
            )
            try:
                tg_file = await doc.get_file()
                file_bytes = await tg_file.download_as_bytearray()
                extracted_text = self.ocr_engine.extract_text_from_image(
                    bytes(file_bytes), mime_type=mime_type
                )
                try:
                    await status_msg.delete()
                except Exception:
                    pass
                await self._audit_and_reply(
                    update=update,
                    evidence_text=extracted_text,
                    provenance=extract_forward_provenance(update.message),
                    media_label=f"Image Document ({doc.file_name})",
                )
                return
            except Exception as e:
                logger.error("Error handling document image: %s", e)

        # Default fallback for other documents
        await update.message.reply_text(
            f"📄 Received file: <b>{html.escape(doc.file_name or 'document')}</b>. "
            "Please send suspicious text messages, screenshots, voice notes, or APK files for fraud evaluation.",
            parse_mode=ParseMode.HTML,
        )

    def build_application(self) -> Application:
        """Build and configure the python-telegram-bot application."""
        app = ApplicationBuilder().token(self.token).build()

        # Commands
        app.add_handler(CommandHandler("start", self.handle_start))
        app.add_handler(CommandHandler("help", self.handle_help))
        app.add_handler(CommandHandler("status", self.handle_status))

        # Media & Messages
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        app.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, self.handle_voice))
        app.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))

        return app

    def run(self) -> None:
        """Run the Telegram Bot in polling mode."""
        app = self.build_application()
        logger.info("SatarkBharat Telegram Bot is starting polling...")
        app.run_polling()


def main():
    """CLI entry point for running the bot."""
    bot = SatarkTelegramBot()
    bot.run()


if __name__ == "__main__":
    main()
