# ONETOO sync v2.1 — verified_tfws (GET-only)

## Goal
Extend sync v2 with a second trust signal:
- `verified`      = ONETOO search found the URL (raw accepted)
- `verified_tfws` = ONETOO search found the URL + TFWS v2 manifest is reachable and parses as JSON

This remains **GET-only**, no tokens, no submit.

## TFWS v2 probe
For a given `target_url`, compute:
- `origin = scheme://netloc`
- `tfws_v2_url = origin + "/.well-known/tfws-v2.json"`

Success condition:
- HTTP status == 200
- Body parses as JSON (dict/object)

Failure:
- Any non-200 / parse error / timeout / DNS error
- => DO NOT set overall status to error. Keep `verified`.

## Ledger fields (recommended)
Keep existing fields from v2, and add:

- `tfws_v2_url`    (string)
- `tfws_v2_http`   (int, optional)
- `tfws_v2_ok`     (bool)
- `tfws_v2_error`  (string, optional, short <= 160 chars)

Example item:
```json
{
  "status": "verified_tfws",
  "status_raw": "accepted",
  "http": 200,
  "checked_utc": "2026-01-14T20:08:03Z",
  "tfws_v2_url": "https://hgpedu.eu/.well-known/tfws-v2.json",
  "tfws_v2_http": 200,
  "tfws_v2_ok": true
}
```

## UI changes
In `pages/portal.html` and `en/pages/portal.html`:
- Add legend entry: `VERIFIED_TFWS`
- Add badge mapping for `verified_tfws`

Minimal semantics:
- `verified_tfws` should appear as "stronger" than `verified`
- Do not break back-compat: old `accepted` should still render as `verified`.

## Back-compat
If ledger still contains `accepted`, UI must render it as `verified`.
v2.1 only adds a higher tier when TFWS check succeeds.
