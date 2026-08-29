#!/usr/bin/env bash
set -euo pipefail

if [[ -f frontend/package-lock.json ]]; then
  npm ci --prefix frontend --no-audit --no-fund
fi

if [[ -f pyproject.toml && -f uv.lock ]]; then
  uv sync --locked --no-progress
elif [[ -f backend/requirements.txt ]]; then
  uv pip install --system --no-progress -r backend/requirements.txt
fi

npm run build --prefix frontend
rm -f frontend/tsconfig.tsbuildinfo
PYTHONPATH=backend python -m compileall -q backend/app