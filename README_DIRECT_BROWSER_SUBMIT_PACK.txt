HGPEdu Portal – Direct Browser Submit Pack (EXPERIMENTAL)

Goal
----
Enable "direct submit from browser" to ONETOO using fetch(), WITHOUT embedding a long-lived secret token in the client.

Reality check
-------------
1) If the ONETOO submit endpoint requires a maintainer token, a true direct-from-browser submit
   is not safely possible (token would leak).
2) This pack implements a tokenless model:
   - client-side cryptographic signature (WebCrypto ECDSA P-256)
   - optional client-side Proof-of-Work (Hashcash-like)
   - strict client throttling + UX safety rails
   - fire-and-forget submit using Content-Type: text/plain to avoid preflight
   - result is verified later via your existing CI ledger sync workflow

What this pack changes
----------------------
- Adds direct submit UI to:
  * pages/portal.html
  * en/pages/portal.html
- Adds JS module:
  * assets/onetoo-submit.js
- Adds docs:
  * docs/direct-browser-submit.md
- Adds patch/apply script:
  * scripts/apply_direct_browser_submit_pack.sh
- Adds python patcher:
  * tools/patch_portal_direct_submit.py

How to apply
------------
Unzip into repo root, then (Git Bash):
  bash scripts/apply_direct_browser_submit_pack.sh

Then:
  git add -A
  git commit -m "feat(portal): experimental direct browser submit to ONETOO (signed+pow)"
  git pull --rebase
  git push

Then test:
  Open https://www.hgpedu.eu/pages/portal
  Fill form -> JSON -> "Submit to ONETOO"

IMPORTANT
---------
You must configure/confirm the ONETOO public submit endpoint in:
  assets/onetoo-submit.js  (CFG.ONETOO_SUBMIT_URL)

If the endpoint does not allow public POST (or blocks CORS response),
the UI will show "SENT (OPAQUE)" and CI ledger will remain the truth.
