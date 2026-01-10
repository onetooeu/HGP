#!/usr/bin/env bash
set -euo pipefail
: "${MINISIGN_SECRET:?set MINISIGN_SECRET to path of minisign secret key}"
test -f "$MINISIGN_SECRET"
test -f ".well-known/sha256.json"
minisign -S -s "$MINISIGN_SECRET" -m ".well-known/sha256.json" -x ".well-known/sha256.json.minisig"
echo "OK: signed .well-known/sha256.json"
