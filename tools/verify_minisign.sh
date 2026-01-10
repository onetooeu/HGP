#!/usr/bin/env bash
set -euo pipefail
test -f ".well-known/minisign.pub"
test -f ".well-known/sha256.json"
test -f ".well-known/sha256.json.minisig"
minisign -Vm ".well-known/sha256.json" -x ".well-known/sha256.json.minisig" -p ".well-known/minisign.pub"
echo "OK: verified .well-known/sha256.json"
