#!/usr/bin/env bash
set -euo pipefail

# Signs .well-known/sha256.json into .well-known/sha256.json.minisig
# Requires minisign and a secret key path passed via MINISIGN_SECRET.
#
# Example:
#   MINISIGN_SECRET=./minisign.key bash tools/sign_minisign.sh

if ! command -v minisign >/dev/null 2>&1; then
  echo "minisign not found. Install minisign first." >&2
  exit 1
fi

SECRET="${MINISIGN_SECRET:-}"
if [[ -z "$SECRET" ]]; then
  echo "Set MINISIGN_SECRET to your minisign secret key path (e.g., ./minisign.key)." >&2
  exit 1
fi

minisign -S -s "$SECRET" -m .well-known/sha256.json -x .well-known/sha256.json.minisig
echo "OK: signed .well-known/sha256.json -> .well-known/sha256.json.minisig"
