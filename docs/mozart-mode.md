# Mozart mode (HGPEdu ↔ ONETOO)

## What it means
HGPEdu runs in **Mozart mode**:
- HGPEdu **does not POST** submissions into ONETOO.
- HGPEdu is a **static feed** + **curated index** (`data/portal/index.json`).
- ONETOO presence is displayed **read-only** via a local ledger (`portal/submissions.json`).

## Why
- Deterministic, auditable, no secrets.
- Avoid pushing content automatically.
- Keep governance explicit: humans/curators decide what becomes part of the feed.

## Status ledger
The ledger maps canonical URLs to:
- `accepted` — URL found in ONETOO search results (exact match)
- `missing` — not found (yet)
- `error` — network/API error during check
- `planned` — no record in ledger yet (UI fallback)

Ledger is safe-by-design:
- no tokens
- GET-only
- machine-readable and reproducible
