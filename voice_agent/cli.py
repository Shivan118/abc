from __future__ import annotations

import typer
from rich.console import Console

from .config import AppConfig
from .audio_io import AudioRecorder
from .stt import SpeechToText
from .tts import TextToSpeech
from .agent import run_agent

app = typer.Typer(add_completion=False, help="Voice AI agent CLI using CrewAI")
console = Console()


@app.command()
def text(prompt: str = typer.Option("", "--prompt", "-p", help="Ask once and exit")) -> None:
    """Chat via typed input."""
    config = AppConfig()
    stt = SpeechToText(config)
    tts = TextToSpeech()

    if prompt:
        response = run_agent(prompt, config)
        tts.speak(response)
        return

    console.print("Type 'exit' to quit.")
    while True:
        user_text = stt.transcribe_typed()
        if user_text.lower() in {"exit", "quit", ":q"}:
            break
        if not user_text:
            continue
        response = run_agent(user_text, config)
        tts.speak(response)


@app.command()
def voice(seconds: int = typer.Option(5, "--seconds", "-s", help="Recording length per turn")) -> None:
    """Chat via your microphone (falls back to typed input)."""
    config = AppConfig()
    recorder = AudioRecorder(sample_rate=config.audio.sample_rate, channels=config.audio.channels)
    stt = SpeechToText(config)
    tts = TextToSpeech()

    console.print("Say something after the beep. Type 'exit' to quit.")
    while True:
        if not recorder.is_available():
            console.print("Microphone unavailable; falling back to typed input. Type 'exit' to quit.")
            user_text = stt.transcribe_typed()
        else:
            user_text = None
            audio = recorder.record(seconds=seconds)
            if audio is not None:
                user_text = stt.transcribe_audio(audio, sample_rate=config.audio.sample_rate)
            if not user_text:
                # If STT failed, fallback to typed input
                user_text = stt.transcribe_typed()

        if user_text.lower() in {"exit", "quit", ":q"}:
            break
        if not user_text:
            continue

        response = run_agent(user_text, config)
        tts.speak(response)
