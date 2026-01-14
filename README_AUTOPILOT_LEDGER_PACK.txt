HGPEdu ↔ ONETOO — Autopilot Phase (CI ledger re-sync) PACK
=========================================================

What you get
------------
1) GitHub Actions workflow:
   .github/workflows/hgpedu-onetoo-ledger-sync.yml

2) Commit helper:
   .github/scripts/commit-if-changed.sh

3) Portal UI patcher (idempotent):
   tools/patch_portal_verified_tfws.py
   - adds VERIFIED_TFWS badge to the legend
   - adds verified_tfws color mapping

4) Apply helper:
   scripts/apply_pack.sh

How to use
----------
1) Unzip into repo root (merge folders).
2) In Git Bash:

   bash scripts/apply_pack.sh

3) Commit + push:

   git add -A
   git commit -m "feat(autopilot): CI ledger re-sync + portal VERIFIED_TFWS UI"
   git pull --rebase
   git push

4) GitHub → Actions → run workflow "hgpedu-onetoo-ledger-sync"

Notes
-----
- If your portal already contains VERIFIED_TFWS changes, the patcher prints OK.
- On Windows, executable bits may not persist after unzip; GitHub runner still runs bash scripts fine.
