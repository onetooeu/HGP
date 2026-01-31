ONETOO sync v2 – status → badge evolution
----------------------------------------

Goal
- Keep HGPEdu fully static + trust-first.
- Only read ONETOO public search endpoint.
- Expose a stronger badge for users: VERIFIED = present in ONETOO accepted-set.

Status model
- planned   : no ledger record yet (default in UI)
- missing   : not found in ONETOO search results
- verified  : exact URL match found (raw status was accepted)
- error     : request failed or unexpected response

Ledger fields (per URL)
- status        : planned/missing/verified/error  (UI-friendly)
- status_raw    : accepted/missing/error          (audit of the search decision)
- http          : HTTP code from ONETOO search
- checked_utc   : timestamp of last check
- error         : short error sample only if status == error
