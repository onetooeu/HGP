# Portal status meanings

Portal items show an ONETOO status badge:

- **ACCEPTED** — the exact URL is visible in ONETOO search surface.
- **MISSING** — the URL is not visible (yet) in ONETOO.
- **ERROR** — the check failed (HTTP error / invalid JSON / network timeout).
- **PLANNED** — no ledger record exists yet for this URL (UI fallback).

Notes:
- Status is derived from a **read-only** check (GET-only).
- Canonicalization is important (prefer: no `www`, no `.html`).
