"""Evidentiary Redressal Dossier Generator: Structured JSON, 1930 SMS, and Court-Ready PDF."""

import hashlib
import io
from datetime import UTC, datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from satark_bharat.decision.threat_engine import ThreatReport
from satark_bharat.redressal.router import JurisdictionalRoute, RegulatoryRouter


FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


def _sanitize_pdf_text(text: str) -> str:
    """Sanitize text to guarantee 100% universal PDF compatibility with zero black block glyphs."""
    if not text:
        return ""
    replacements = {
        "₹": "Rs. ",
        "“": "\"",
        "”": "\"",
        "‘": "'",
        "’": "'",
        "—": " - ",
        "–": " - ",
        "…": "...",
        "•": "*",
        "✓": "[OK]",
        "✔": "[OK]",
        "✕": "[X]",
        "✖": "[X]",
        "⚠": "[!]",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Filter out any non-Latin1 / high-Unicode characters that render as black blocks in standard PDF readers
    clean_chars = []
    for ch in text:
        if ord(ch) < 128:
            clean_chars.append(ch)
        elif ord(ch) in range(128, 256):
            try:
                ch.encode("latin-1")
                clean_chars.append(ch)
            except UnicodeEncodeError:
                clean_chars.append(" ")
        else:
            clean_chars.append(" ")
    return "".join(clean_chars)


class DossierGenerator:
    @staticmethod
    def generate_json_dossier(report: ThreatReport, raw_evidence_text: str) -> dict[str, Any]:
        route: JurisdictionalRoute = RegulatoryRouter.resolve_route(report)
        timestamp = datetime.now(UTC).isoformat()
        evidence_hash = hashlib.sha256(raw_evidence_text.encode("utf-8")).hexdigest()

        return {
            "dossier_type": route.dossier_type,
            "incident_id": f"SB-{datetime.now(UTC).strftime('%Y%m%d')}-{evidence_hash[:8].upper()}",
            "generated_at_utc": timestamp,
            "target_portal": {
                "name": route.portal_name,
                "url": route.portal_url,
                "authority": route.target_authority,
                "statutory_basis": route.statutory_basis,
                "routing_rationale": route.routing_rationale,
            },
            "threat_metrics": {
                "composite_threat_score": report.composite_threat_score,
                "severity": report.severity,
                "red_line_triggered": report.red_line_triggered,
                "red_line_reason": report.red_line_reason,
                "penalty_breakdown": report.penalty_breakdown,
            },
            "statutory_violations": report.statutory_violations,
            "extracted_regulatory_tokens": {
                "claimed_sebi_id": report.sebi_audit.claimed_id,
                "sebi_category": report.sebi_audit.category,
                "sebi_registry_status": report.sebi_audit.registry_status,
                "registered_entity_name": report.sebi_audit.registered_entity_name,
                "is_impersonation_suspected": report.sebi_audit.is_impersonation_suspected,
                "recipient_vpas": report.payment_audit.detected_vpas,
                "is_personal_vpa": report.payment_audit.is_personal_vpa,
                "detected_urls": report.domain_audit.detected_urls,
                "has_apk_link": report.domain_audit.has_apk_link,
                "is_domain_typosquatted": report.domain_audit.is_typosquatted,
                "spoofed_domain_target": report.domain_audit.spoofed_target,
            },
            "evidentiary_narrative": {
                "raw_evidence_snippet": raw_evidence_text[:1000],
                "sha256_checksum": evidence_hash,
            },
            "investor_vernacular_advisories": {
                "english": report.plain_english_summary,
                "hindi": report.vernacular_hindi_summary,
                "bengali": report.vernacular_bengali_summary,
            },
        }

    @staticmethod
    def generate_1930_sms(report: ThreatReport, incident_id: str) -> str:
        """Format an instant plain-text dispatch for the 1930 Cyber Fraud Helpline / WhatsApp report."""
        vpa = report.payment_audit.primary_vpa or "None"
        sebi_id = report.sebi_audit.claimed_id or "Unregistered"
        urls = ", ".join(report.domain_audit.detected_urls) if report.domain_audit.detected_urls else "None"

        return (
            f"[CRITICAL FRAUD ALERT - 1930 DISPATCH]\n"
            f"Incident Ref: {incident_id}\n"
            f"Offense: Sec 66D IT Act / SEBI Unregistered Fraud\n"
            f"Suspect Recipient VPA: {vpa}\n"
            f"Claimed Entity / SEBI: {sebi_id}\n"
            f"Phishing Link / APK: {urls}\n"
            f"Threat Score: {report.composite_threat_score}/100 ({report.severity})\n"
            f"Action Required: Freeze beneficiary UPI/Bank account immediately."
        )

    @staticmethod
    def generate_pdf_dossier(dossier_data: dict[str, Any]) -> bytes:
        """Compile a formal court-ready PDF complaint package."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )

        styles = getSampleStyleSheet()
        normal_style = ParagraphStyle(
            "DocNormal",
            parent=styles["Normal"],
            fontName=FONT_REGULAR,
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#1f2937"),
        )
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontName=FONT_BOLD,
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#161614"),
            spaceAfter=4,
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontName=FONT_REGULAR,
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#4b5563"),
            spaceAfter=15,
        )
        section_style = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading2"],
            fontName=FONT_BOLD,
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#1f2937"),
            spaceBefore=12,
            spaceAfter=6,
        )

        table_cell_style = ParagraphStyle(
            "TableCell",
            parent=styles["Normal"],
            fontName=FONT_REGULAR,
            fontSize=8.5,
            leading=11.5,
            textColor=colors.HexColor("#1f2937"),
        )
        table_cell_bold = ParagraphStyle(
            "TableCellBold",
            parent=styles["Normal"],
            fontName=FONT_BOLD,
            fontSize=8.5,
            leading=11.5,
            textColor=colors.HexColor("#374151"),
        )

        story = []

        # Header Title (Clean English to avoid missing glyphs in PDF viewers)
        story.append(Paragraph("<b>SATARK BHARAT</b>", title_style))
        story.append(Paragraph("EVIDENTIARY REGULATORY GRIEVANCE &amp; CYBER FRAUD INCIDENT DOSSIER", subtitle_style))
        story.append(Spacer(1, 10))

        # Incident Metadata Table (Cells wrapped in Paragraphs for text wrapping)
        meta_raw = [
            ("Incident Reference ID:", str(dossier_data["incident_id"])),
            ("Generated Timestamp (UTC):", str(dossier_data["generated_at_utc"])),
            ("Designated Redressal Portal:", str(dossier_data["target_portal"]["name"])),
            ("Primary Authority:", str(dossier_data["target_portal"]["authority"])),
            ("Statutory Jurisdiction:", str(dossier_data["target_portal"]["statutory_basis"])),
            ("Composite Threat Score:", f"{dossier_data['threat_metrics']['composite_threat_score']}/100 ({dossier_data['threat_metrics']['severity']})"),
        ]
        meta_data = [
            [Paragraph(_sanitize_pdf_text(lbl), table_cell_bold), Paragraph(_sanitize_pdf_text(val), table_cell_style)]
            for lbl, val in meta_raw
        ]
        meta_table = Table(meta_data, colWidths=[160, 360])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 15))

        # Regulatory Violations Section
        story.append(Paragraph("<b>1. Statutory &amp; Regulatory Violations Detected</b>", section_style))
        violations = dossier_data.get("statutory_violations", [])
        if violations:
            for v in violations:
                clean_v = _sanitize_pdf_text(v)
                story.append(Paragraph(f"• {clean_v}", normal_style))
                story.append(Spacer(1, 3))
        else:
            story.append(Paragraph("No direct regulatory infractions recorded.", normal_style))
        story.append(Spacer(1, 10))

        # Extracted Regulatory Invariants Section
        story.append(Paragraph("<b>2. Extracted Regulatory Invariants &amp; Entities</b>", section_style))
        tokens = dossier_data["extracted_regulatory_tokens"]
        token_raw = [
            ("Claimed SEBI Reg ID:", str(tokens.get("claimed_sebi_id") or "None (Unregistered)")),
            ("Registry Verification Status:", str(tokens.get("sebi_registry_status"))),
            ("Registered Name on SEBI Master:", str(tokens.get("registered_entity_name") or "N/A")),
            ("Identity Impersonation Suspected:", str(tokens.get("is_impersonation_suspected"))),
            ("Solicited Recipient UPI VPA:", ", ".join(tokens.get("recipient_vpas", [])) or "None"),
            ("Personal VPA (Clearance Violation):", str(tokens.get("is_personal_vpa"))),
            ("Typosquatted Lookalike Domain:", str(tokens.get("is_domain_typosquatted"))),
            ("Malicious APK File Link:", str(tokens.get("has_apk_link"))),
        ]
        token_data = [
            [Paragraph(_sanitize_pdf_text(lbl), table_cell_bold), Paragraph(_sanitize_pdf_text(val), table_cell_style)]
            for lbl, val in token_raw
        ]
        token_table = Table(token_data, colWidths=[160, 360])
        token_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#ffffff")),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ]))
        story.append(token_table)
        story.append(Spacer(1, 15))

        # Raw Evidentiary Narrative Section
        story.append(Paragraph("<b>3. Raw Evidentiary Extract &amp; Cryptographic Hash</b>", section_style))
        sha = dossier_data["evidentiary_narrative"]["sha256_checksum"]
        raw = _sanitize_pdf_text(dossier_data["evidentiary_narrative"]["raw_evidence_snippet"]).replace("\n", " ")
        story.append(Paragraph(f"<b>SHA-256 Digest:</b> <code>{sha}</code>", normal_style))
        story.append(Spacer(1, 5))
        story.append(Paragraph(f"<b>Extract:</b> <i>\"{raw}\"</i>", normal_style))
        story.append(Spacer(1, 15))

        # Disclaimer
        story.append(Paragraph(
            "<font size=8 color='#6b7280'>Automated regulatory dossier compiled by SatarkBharat Sentinel Engine. "
            "Formulated for institutional submission to SEBI SCORES 2.0 and the National Cyber Crime Reporting Portal (NCRP / Helpline 1930). "
            "Zero generative stock recommendations or investment solicitations are provided.</font>",
            normal_style
        ))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
