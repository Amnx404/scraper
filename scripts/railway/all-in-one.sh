#!/usr/bin/env bash
set -euo pipefail

# NOTE: This runs BOTH web + worker in one container.
# Railway supports this, but two separate services is more reliable.

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

procrastinate --app=live.worker.app.procrastinate_app schema --apply || true

procrastinate --app=live.worker.app.procrastinate_app worker &
WORKER_PID=$!

cleanup() {
  if kill -0 "$WORKER_PID" 2>/dev/null; then
    kill "$WORKER_PID" || true
  fi
}
trap cleanup EXIT INT TERM

exec python -m uvicorn live.api.main:app --host "$HOST" --port "$PORT"
