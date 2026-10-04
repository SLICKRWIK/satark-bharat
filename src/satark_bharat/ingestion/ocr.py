"""Visual OCR & Screenshot Ingestion Module (Gemini Multimodal Sentinel + Local Fallback)."""

import base64
import io
import os
from pathlib import Path

from PIL import Image

from satark_bharat.config import PROJECT_ROOT


class VisualOcrIngestion:
    """Multimodal Vision and OCR ingestion for scam screenshots."""

    def __init__(self):
        self._easyocr_reader = None
        self._init_attempted = False

    def _get_gemini_api_key(self) -> str | None:
        """Retrieve Gemini API key from Streamlit secrets, environment, or project .env file."""
        # 1. Check Streamlit Cloud secrets
        try:
            import streamlit as st

            if hasattr(st, "secrets"):
                if "GEMINI_API_KEY" in st.secrets:
                    return str(st.secrets["GEMINI_API_KEY"]).strip()
                if "GOOGLE_API_KEY" in st.secrets:
                    return str(st.secrets["GOOGLE_API_KEY"]).strip()
        except Exception:
            pass

        # 2. Check environment variables
        key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if key:
            return key.strip()

        # 3. Check local .env file
        env_paths = [PROJECT_ROOT / ".env", Path(".env")]
        for env_path in env_paths:
            if env_path.exists():
                try:
                    for line in env_path.read_text(encoding="utf-8").splitlines():
                        line = line.strip()
                        if line.startswith("GEMINI_API_KEY="):
                            return line.split("=", 1)[1].strip()
                        if line.startswith("GOOGLE_API_KEY="):
                            return line.split("=", 1)[1].strip()
                except Exception:
                    pass
        return None

    def _get_reader(self):
        """Lazy load local EasyOCR engine if installed."""
        if not self._init_attempted:
            self._init_attempted = True
            try:
                import easyocr

                self._easyocr_reader = easyocr.Reader(["en", "hi"], gpu=False)
            except Exception:
                self._easyocr_reader = None
        return self._easyocr_reader

    def extract_with_gemini(self, image_bytes: bytes, mime_type: str = "image/png") -> str | None:
        """Call Gemini Multimodal Vision to extract text and regulatory tokens from an image."""
        api_key = self._get_gemini_api_key()
        if not api_key:
            return None

        try:
            import requests

            b64_image = base64.b64encode(image_bytes).decode("utf-8")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"

            prompt = (
                "You are the SatarkBharat Multimodal Sentinel. "
                "Carefully transcribe all readable text, chat messages, advisory calls, stock tickers, "
                "entry/target prices, claimed SEBI registration numbers, UPI VPAs, phone numbers, "
                "and links visible in this screenshot. "
                "Preserve all tokens verbatim without hallucination or omitting numbers."
            )

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {"inline_data": {"mime_type": mime_type, "data": b64_image}},
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.0,
                },
            }

            resp = requests.post(url, json=payload, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    extracted_text = "".join(part.get("text", "") for part in parts).strip()
                    if extracted_text:
                        return extracted_text
        except Exception:
            pass
        return None

    def extract_text_from_image(self, image_bytes: bytes, mime_type: str = "image/png") -> str:
        """Extract text from screenshot bytes using Gemini Vision or local OCR fallback."""
        if not image_bytes:
            return ""

        # Validate that image_bytes is a valid image
        try:
            with Image.open(io.BytesIO(image_bytes)) as img:
                img.verify()
        except Exception as e:
            return f"[Error: Uploaded file is not a valid image format: {e}]"

        # 1. Primary: Google Gemini Multimodal Vision
        gemini_result = self.extract_with_gemini(image_bytes, mime_type=mime_type)
        if gemini_result:
            return gemini_result

        # 2. Secondary: Local EasyOCR if installed
        try:
            reader = self._get_reader()
            if reader:
                results = reader.readtext(image_bytes)
                extracted_lines = [res[1] for res in results]
                if extracted_lines:
                    return "\n".join(extracted_lines)
        except Exception:
            pass

        # 3. Fallback message if neither model could run
        return (
            "[Notice: OCR requires GEMINI_API_KEY in .env or easyocr installed. "
            "Please paste the text directly into the Advisory Text tab or select a sample scenario above.]"
        )
