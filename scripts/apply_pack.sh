#!/usr/bin/env bash
set -euo pipefail

echo "== HGPEdu Autopilot Ledger Pack: apply =="

if command -v chmod >/dev/null 2>&1; then
  chmod +x .github/scripts/commit-if-changed.sh || true
  chmod +x tools/patch_portal_verified_tfws.py || true
fi

python tools/patch_portal_verified_tfws.py pages/portal.html en/pages/portal.html || true

echo
echo "Next steps (Git Bash):"
echo "  git add -A"
echo "  git commit -m \"feat(autopilot): CI ledger re-sync + portal VERIFIED_TFWS UI\""
echo "  git pull --rebase"
echo "  git push"
echo
echo "Then in GitHub -> Actions, run workflow: hgpedu-onetoo-ledger-sync"
