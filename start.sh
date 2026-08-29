#!/usr/bin/env bash
set -euo pipefail

cleanup() {
  if [[ -n "${BACKEND_PID:-}" ]]; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi
}

trap cleanup EXIT INT TERM

PYTHONPATH=backend python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

for _ in {1..40}; do
  if curl -fsS http://127.0.0.1:8000/api/health >/dev/null 2>&1; then
    break
  fi
  sleep 0.25
done

cd frontend
npm run dev -- --host 0.0.0.0 --port 5000