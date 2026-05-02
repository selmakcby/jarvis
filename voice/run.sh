#!/usr/bin/env bash
# Loads OPENAI_API_KEY from ~/.openclaw/secrets.env and runs the Jarvis voice daemon.
# Usage: ~/Jarvis/voice/run.sh

set -e

SECRETS=~/.openclaw/secrets.env
if [ -f "$SECRETS" ]; then
  set -a
  source "$SECRETS"
  set +a
fi

if [ -z "$OPENAI_API_KEY" ]; then
  echo "error: OPENAI_API_KEY not set (expected in $SECRETS or env)"
  exit 1
fi

exec python3 ~/Jarvis/voice/jarvis_voice.py
