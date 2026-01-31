#!/usr/bin/env bash
set -euo pipefail

echo "== HGPEdu Direct Browser Submit Pack: apply =="

# Sanity checks
if [ ! -f "pages/portal.html" ]; then
  echo "Missing pages/portal.html"
  exit 1
fi

if [ ! -f "en/pages/portal.html" ]; then
  echo "Missing en/pages/portal.html"
  exit 1
fi

# Ensure dirs exist (some packs drop files here)
mkdir -p assets docs tools scripts

# Patch portals (expects the python script to exist)
if [ ! -f "tools/patch_portal_direct_submit.py" ]; then
  echo "Missing tools/patch_portal_direct_submit.py"
  exit 1
fi

python tools/patch_portal_direct_submit.py pages/portal.html en/pages/portal.html

echo "OK: patched portal pages."
echo
echo "Next steps:"
echo "  git add -A"
echo "  git commit -m 'feat(portal): experimental direct browser submit to ONETOO (signed+pow)'"
echo "  git pull --rebase"
echo "  git push"
echo
echo "IMPORTANT: configure assets/onetoo-submit.js -> CFG.ONETOO_SUBMIT_URL"