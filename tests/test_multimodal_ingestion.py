"""Tests for Multimodal Ingestion (Vision & Audio Sentinels)."""

import io

from PIL import Image

from satark_bharat.ingestion.audio import AudioIngestionModule
from satark_bharat.ingestion.ocr import VisualOcrIngestion


def test_ocr_invalid_image_bytes():
    ocr = VisualOcrIngestion()
    res = ocr.extract_text_from_image(b"not_an_image")
    assert "Error: Uploaded file is not a valid image format" in res


def test_ocr_valid_image_structure():
    ocr = VisualOcrIngestion()
    # Generate a simple valid image in-memory
    img = Image.new("RGB", (200, 100), color=(73, 109, 137))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    res = ocr.extract_text_from_image(buf.getvalue())
    assert isinstance(res, str)
    assert len(res) > 0


def test_audio_ingestion_valid_call():
    audio_mod = AudioIngestionModule()
    res = audio_mod.transcribe_audio(b"dummy_bytes", filename="test.mp3")
    assert isinstance(res, str)
    assert len(res) > 0
