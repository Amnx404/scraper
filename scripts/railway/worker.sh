#!/usr/bin/env bash
set -euo pipefail

# Ensure schema exists (idempotent-ish; if it errors because types exist, you can remove this line)
procrastinate --app=live.worker.app.procrastinate_app schema --apply || true

exec procrastinate --app=live.worker.app.procrastinate_app worker
