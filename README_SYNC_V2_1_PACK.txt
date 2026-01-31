🧭 HGP / ONETOO — SYNC v2.1 ADD-ON (verified_tfws) — GET-only
Date: 2026-01-14
Purpose:
  - Extend existing ONETOO sync v2 to v2.1 by adding a second, GET-only trust signal:
      verified_tfws = URL found in ONETOO search + TFWS v2 manifest is reachable and parses as JSON.

IMPORTANT GUARANTEES
  - Still GET-only. No tokens. No submit. No POST.
  - TFWS check is "bonus signal" only:
      - If TFWS check fails, status stays "verified" (NOT "error").
      - "error" is reserved for failures of the ONETOO lookup or internal script errors.

WHAT'S IN THIS ZIP
  1) tools/tfws_v2_probe.py
     - Small helper you can import from tools/onetoo_status_sync.py.
  2) docs/onetoo-sync-v2.1.md
     - Implementation notes + expected ledger fields.
  3) snippets/
     - HTML snippets to paste into pages/portal.html and en/pages/portal.html:
         - legend entry for VERIFIED_TFWS
         - minimal badge mapping note (where to add "verified_tfws")

HOW TO APPLY (recommended)
  0) Unzip into the ROOT of your repo (same level as pages/, tools/, docs/).
  1) Edit tools/onetoo_status_sync.py:
     - Import helper:
         from tools.tfws_v2_probe import tfws_v2_check
     - When raw_status == "accepted" (=> you set status="verified"):
         call tfws_v2_check(target_url) and if ok -> status="verified_tfws"
     - Persist fields into ledger item (see docs/onetoo-sync-v2.1.md).
  2) Edit pages/portal.html + en/pages/portal.html:
     - Add legend line for VERIFIED_TFWS (use snippets).
     - Add UI mapping for status "verified_tfws" (badge label + style).
  3) Run tests:
     python -m py_compile tools/onetoo_status_sync.py
     python tools/onetoo_status_sync.py --limit 5
     head -n 160 portal/submissions.json
  4) Commit & push:
     git add -A
     git commit -m "feat(onetoo): sync v2.1 verified_tfws (GET-only TFWS v2 check)"
     git pull --rebase
     git push

NOTES
  - TFWS URL used:
      https://<origin>/.well-known/tfws-v2.json
  - "origin" is derived from the target_url (scheme + netloc).
