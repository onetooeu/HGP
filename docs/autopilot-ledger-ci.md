# HGPEdu ↔ ONETOO Ledger Autopilot (CI)

This pack adds a GitHub Actions workflow that periodically regenerates:

- `portal/submissions.json`

by calling the existing GET-only tool:

- `python tools/onetoo_status_sync.py`

## What it does

- Runs every 6 hours (cron) + can be run manually (workflow_dispatch).
- Deletes the current ledger file, regenerates it, and commits only if changed.
- Uses `contents: write` permission (repo setting must allow actions to push).

## Safety

- GET-only calls (no tokens, no submit endpoints).
- Only writes `portal/submissions.json`.

## Install

Copy files into repo root (merge folders), then run:

```bash
bash scripts/apply_pack.sh
```

Commit & push.

## Verify

In GitHub:
Actions → **hgpedu-onetoo-ledger-sync** → Run workflow

Then check the latest commit message:
`chore(autopilot): refresh ONETOO ledger [skip ci]`
