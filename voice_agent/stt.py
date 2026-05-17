from __future__ import annotations

import io
import os
import tempfile
from typing import Optional

from .config import AppConfig

try:
    # OpenAI python SDK v1.x
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore

try:
    import soundfile as sf  # type: ignore
except Exception:  # pragma: no cover
    sf = None  # type: ignore


class SpeechToText:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.client = OpenAI(api_key=config.llm.api_key) if (OpenAI and config.llm.api_key) else None

    def transcribe_audio(self, audio: Optional["np.ndarray"], sample_rate: int) -> Optional[str]:
        if self.client is None or audio is None or sf is None:
            return None
        try:
            # Write to a temporary wav file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
                sf.write(tmp.name, audio, sample_rate)
                with open(tmp.name, "rb") as f:
                    result = self.client.audio.transcriptions.create(model=os.getenv("OPENAI_STT_MODEL", "whisper-1"), file=f)
            text = getattr(result, "text", None)
            if isinstance(text, str) and text.strip():
                return text.strip()
        except Exception:
            return None
        return None

    def transcribe_typed(self) -> str:
        try:
            return input("You: ").strip()
        except EOFError:
            return ""
