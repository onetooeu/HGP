# Hardening Summary (Final Boss)

This site is static-first and intentionally minimal.

## Enabled
- Strict security headers via `_headers`
- CSP restricting scripts and connections (only self + ONETOO endpoints)
- No tracking pixels, no third-party analytics scripts
- Integrity inventory via `.well-known/sha256.json`
- Optional minisign signing for integrity inventory

## Recommended
- Keep minisign secret key offline (never commit it).
- Rotate keys via `.well-known/key-history.json` when needed.
- Tag releases and keep them immutable.
