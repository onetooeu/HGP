#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   bash .github/scripts/commit-if-changed.sh [file] [message]
FILE="${1:-}"
MSG="${2:-"chore: update [skip ci]"}"

git config user.name  "${GIT_AUTHOR_NAME:-hgpedu-bot}"
git config user.email "${GIT_AUTHOR_EMAIL:-actions@users.noreply.github.com}"

# Stage changes
if [[ -n "$FILE" ]]; then
  git add "$FILE"
else
  git add -A
fi

# Nothing to commit
if git diff --cached --quiet; then
  echo "No changes"
  exit 0
fi

git commit -m "$MSG" || { echo "No changes"; exit 0; }

# Push with rebase+retry to avoid non-fast-forward races
for i in 1 2 3 4 5; do
  git fetch --prune origin main

  if ! git rebase "origin/main"; then
    git rebase --abort || true
    echo "Rebase failed"
    exit 1
  fi

  if git push origin HEAD:main; then
    echo "Pushed OK"
    exit 0
  fi

  echo "Push rejected (race). Retry $i/5..."
  sleep $((i*2))
done

echo "Push failed after retries"
exit 1
