#!/usr/bin/env bash
set -euo pipefail

FILE="portal/submissions.json"

if git diff --quiet -- "$FILE"; then
  echo "No changes in $FILE — nothing to commit."
  exit 0
fi

git config user.name  "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

git add "$FILE"
git commit -m "chore(autopilot): refresh ONETOO ledger [skip ci]"
git push
echo "Pushed updated $FILE"
