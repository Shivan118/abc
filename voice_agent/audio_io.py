from __future__ import annotations

import contextlib
from typing import Optional

try:
    import sounddevice as sd  # type: ignore
    import numpy as np
except Exception:  # pragma: no cover
    sd = None  # type: ignore
    np = None  # type: ignore


class AudioRecorder:
    def __init__(self, sample_rate: int = 16000, channels: int = 1) -> None:
        self.sample_rate = sample_rate
        self.channels = channels

    def is_available(self) -> bool:
        return sd is not None

    def record(self, seconds: int = 5) -> Optional["np.ndarray"]:
        if sd is None or np is None:
            return None
        with contextlib.suppress(Exception):
            recording = sd.rec(int(seconds * self.sample_rate), samplerate=self.sample_rate, channels=self.channels, dtype="float32")
            sd.wait()
            return recording
        return None
