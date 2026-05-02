# Jarvis Voice — wake-word daemon

A Python daemon that lets Selma talk to [[IDENTITY|Jarvis]] hands-free. Says **"hey jarvis"**, talks, gets a spoken reply.

## Stack (fully open-source wake word, no signup needed)

| Component | Tool | Cost |
|---|---|---|
| Wake word | **OpenWakeWord** (`hey_jarvis` pretrained) | **Free, runs offline** |
| Speech → Text | OpenAI Whisper API | ~$0.006/min |
| Brain | gpt-4o-mini | ~$0.0001/reply |
| Text → Speech | macOS `say` (Samantha voice) | **Free** |

## Flow

```
🎤 listens for "hey jarvis"
    ↓
✨ detected → chime
    ↓
🎙️  records 6s of speech
    ↓
📝 OpenAI Whisper transcribes
    ↓
🧠 gpt-4o-mini answers as Jarvis
    ↓
🔊 macOS `say` speaks the reply
    ↓
💾 logs to memory/voice-YYYY-MM-DD.md (Claude Code can read it)
```

## Why this matters

This is the missing piece that makes Jarvis feel like Jarvis, not a CLI. Every interaction is also written to the shared memory folder — so [[CLAUDE|Claude Code at the desk]] knows what Selma said via voice.

## Run

```bash
~/Jarvis/voice/run.sh
```

macOS will prompt for **microphone permission the first time** — click Allow.

## Stop

Ctrl+C in the terminal running it.

## Cost per interaction

~$0.005 — half a cent. Wake word and TTS are free; only Whisper + gpt-4o-mini call cost anything.
