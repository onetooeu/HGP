#!/usr/bin/env bash
set -euo pipefail

# Verifies .well-known/sha256.json against .well-known/sha256.json.minisig
# Uses .well-known/minisign.pub

if ! command -v minisign >/dev/null 2>&1; then
  echo "minisign not found. Install minisign first." >&2
  exit 1
fi

minisign -Vm .well-known/sha256.json -x .well-known/sha256.json.minisig -p .well-known/minisign.pub
echo "OK: verified"
