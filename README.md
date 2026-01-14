# HGP Edu Portal

Static TFWS v2 / ONETOO showcase portal.

## Portal Autopilot

Create an Issue titled `[PORTAL] ...` using the template. Autopilot validates JSON and publishes to `data/portal/index.json`.

## ONETOO Submit Autopilot

After portal publishing, the repo can periodically sync a local ONETOO *status ledger* (read-only) using `tools/onetoo_submit.py` and the GitHub Action `onetoo-status-sync`.

Docs: `/pages/onetoo-integration.html`

## Docs

- `docs/ONETOO_STANDARD_2026.md` — how HGPEdu integrates with ONETOO Standard 2026 (read-only public runtime)
- `docs/MOZART_MODE.md` — final tuning checklist for a coherent trust-first portal
