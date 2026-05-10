#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "[*] exporting OpenAPI schema from FastAPI..."
cd "$REPO_ROOT/backend"
uv run python scripts/openapi-export.py > "$REPO_ROOT/openapi.json"
echo "[+] schema exported to openapi.json"

echo "[*] generating frontend API client..."
cd "$REPO_ROOT/frontend"
pnpm generate:api

echo "[+] done. Generated files in frontend/src/api/"
