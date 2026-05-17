from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class LLMConfig:
    model: str = os.getenv("LLM_MODEL", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    provider: str = os.getenv("LLM_PROVIDER", "openai")
    api_key: Optional[str] = os.getenv("OPENAI_API_KEY")


@dataclass(frozen=True)
class AudioConfig:
    sample_rate: int = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
    channels: int = int(os.getenv("AUDIO_CHANNELS", "1"))
    record_seconds: int = int(os.getenv("AUDIO_RECORD_SECONDS", "5"))


@dataclass(frozen=True)
class AppConfig:
    llm: LLMConfig = LLMConfig()
    audio: AudioConfig = AudioConfig()
    verbose: bool = os.getenv("VERBOSE", "0") == "1"
