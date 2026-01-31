#!/usr/bin/env bash
set -euo pipefail

BASE="${1:-https://hgpedu.eu}"

echo "== Portal page =="
curl -sSI "$BASE/pages/portal" | head -n 20

echo
echo "== Portal feed index =="
curl -sS "$BASE/data/portal/index.json" | head -n 40

echo
echo "== Status ledger =="
curl -sS "$BASE/portal/submissions.json" | head -n 60

echo
echo "OK"
