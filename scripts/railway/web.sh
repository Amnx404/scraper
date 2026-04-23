#!/usr/bin/env bash
set -euo pipefail

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

exec uv run uvicorn live.api.main:app --host "$HOST" --port "$PORT"
