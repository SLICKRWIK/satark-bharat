"""Vernacular Text-to-Speech (TTS) Voice Alert Generator."""

import io

from gtts import gTTS


class VernacularVoiceEngine:
    def __init__(self):
        self._cache = {}

    def synthesize(self, text: str, lang: str = "hi") -> bytes | None:
        """Synthesize text into MP3 audio bytes with local in-memory caching."""
        cache_key = f"{lang}:{text}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            audio_bytes = fp.getvalue()
            self._cache[cache_key] = audio_bytes
            return audio_bytes
        except Exception:
            # Graceful network or local fallback
            return None
