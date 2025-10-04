from __future__ import annotations

from typing import Optional

try:
    import pyttsx3  # type: ignore
except Exception:  # pragma: no cover
    pyttsx3 = None  # type: ignore


class TextToSpeech:
    def __init__(self) -> None:
        self.engine = None
        if pyttsx3 is not None:
            try:
                self.engine = pyttsx3.init()
            except Exception:
                self.engine = None

    def speak(self, text: str) -> None:
        if not text:
            return
        if self.engine is not None:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
                return
            except Exception:
                pass
        print(f"Agent: {text}")
