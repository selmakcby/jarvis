#!/usr/bin/env python3
"""
Jarvis voice wake-word daemon (OpenWakeWord version).

Listens for "Hey Jarvis" via OpenWakeWord (fully open-source, offline, no API key).
Records ~6s of speech, transcribes with OpenAI Whisper,
sends to gpt-4o-mini with Jarvis personality, speaks the response
via macOS `say`, and logs each interaction to ~/Jarvis/memory/voice-YYYY-MM-DD.md
so Claude Code can read what was said when invoked from ~/Jarvis.

Run: python3 ~/Jarvis/voice/jarvis_voice.py   (or ./run.sh)
Stop: Ctrl+C
"""

import datetime
import io
import os
import subprocess
import sys
import time
import wave
from pathlib import Path

import numpy as np
import sounddevice as sd
from openai import OpenAI
from openwakeword.model import Model

JARVIS_HOME = Path.home() / "Jarvis"
MEMORY_DIR = JARVIS_HOME / "memory"
WAKE_MODEL = "hey_jarvis"             # OpenWakeWord pretrained model
WAKE_THRESHOLD = 0.5                  # confidence threshold for trigger
WAKE_COOLDOWN_SEC = 2                 # avoid double-triggers
SAMPLE_RATE = 16000                   # OWW expects 16 kHz mono
FRAME_LENGTH = 1280                   # 80 ms at 16 kHz
RECORD_SECONDS = 6

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_KEY:
    sys.exit("error: set OPENAI_API_KEY in env or ~/.openclaw/secrets.env")

client = OpenAI(api_key=OPENAI_KEY)

JARVIS_SYSTEM = (
    "You are Jarvis, Selma's calm, dry, life-side AI assistant. "
    "This is voice mode — keep replies to 1-2 short sentences. "
    "Skip filler ('great question', 'happy to help'). Direct answers only. "
    "You handle life automation, not coding."
)


def chime():
    subprocess.run(["afplay", "/System/Library/Sounds/Tink.aiff"], check=False)


def speak(text: str):
    # Daniel: classic British male, the closest macOS-built-in voice to "Jarvis"
    subprocess.run(["say", "-v", "Daniel", text], check=False)


def record(seconds: int) -> np.ndarray:
    print(f"  recording {seconds}s of speech…")
    audio = sd.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE,
                   channels=1, dtype="int16")
    sd.wait()
    return audio.flatten()


def transcribe(audio: np.ndarray) -> str:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(audio.tobytes())
    buf.seek(0)
    buf.name = "speech.wav"
    res = client.audio.transcriptions.create(model="whisper-1", file=buf)
    return (res.text or "").strip()


def ask_jarvis(user_text: str) -> str:
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": JARVIS_SYSTEM},
            {"role": "user", "content": user_text},
        ],
    )
    return (res.choices[0].message.content or "").strip()


def log_interaction(user_text: str, jarvis_text: str):
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    log_file = MEMORY_DIR / f"voice-{datetime.date.today().isoformat()}.md"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(f"\n## {datetime.datetime.now().strftime('%H:%M:%S')}\n\n")
        f.write(f"**Selma (voice):** {user_text}\n\n")
        f.write(f"**Jarvis:** {jarvis_text}\n")


def main():
    print("🦾 Jarvis voice — loading wake-word model…")
    oww = Model(wakeword_models=[WAKE_MODEL], inference_framework="onnx")
    print(f"   wake word: 'hey jarvis'  |  threshold: {WAKE_THRESHOLD}")
    print(f"   sample rate: {SAMPLE_RATE} Hz, frame: {FRAME_LENGTH}")
    print("   Ctrl+C to stop")
    print()
    print("🎤 listening for 'hey jarvis'…")

    last_trigger = 0.0

    try:
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=FRAME_LENGTH,
            dtype="int16",
            channels=1,
        ) as stream:
            while True:
                pcm_bytes, _ = stream.read(FRAME_LENGTH)
                pcm = np.frombuffer(pcm_bytes, dtype=np.int16)

                prediction = oww.predict(pcm)
                score = prediction.get(WAKE_MODEL, 0.0)

                now = time.monotonic()
                if score < WAKE_THRESHOLD or (now - last_trigger) < WAKE_COOLDOWN_SEC:
                    continue

                last_trigger = now
                print(f"\n✨ Wake word detected (score={score:.2f}).")
                chime()

                # release the wake-word stream while we record speech
                stream.stop()
                audio = record(RECORD_SECONDS)
                stream.start()

                try:
                    user_text = transcribe(audio)
                except Exception as e:
                    print(f"  transcription error: {e}")
                    speak("Sorry, I had trouble hearing that.")
                    continue

                print(f"  you: {user_text!r}")
                if not user_text:
                    speak("I didn't catch that.")
                    continue

                try:
                    reply = ask_jarvis(user_text)
                except Exception as e:
                    print(f"  llm error: {e}")
                    speak("I had trouble thinking just then.")
                    continue

                print(f"  jarvis: {reply!r}")
                log_interaction(user_text, reply)
                speak(reply)
                print("\n🎤 listening for 'hey jarvis' again…")

                # reset OWW internal buffer so next detection is clean
                oww.reset()
    except KeyboardInterrupt:
        print("\nbye 🦾")


if __name__ == "__main__":
    main()
