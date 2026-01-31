# Direct browser submit to ONETOO (experimental)

This feature is **experimental** and intentionally designed for an **AI-first** usage pattern:
- "Submit" is *fire-and-forget*.
- Truth is confirmed later via the **CI ledger sync** (`portal/submissions.json`).

## Why no token in the browser?
A long-lived maintainer token in client JS would leak and enable abuse.

So we use a **tokenless** model:
- each submission contains a **public-key signature**
- optional **Proof-of-Work** (PoW) to slow down spam
- later verification is done by ONETOO + your CI ledger

## ONETOO endpoint requirements

For browser-direct submit to work end-to-end, ONETOO must accept **public POST** to a submit endpoint, e.g.:

`POST https://search.onetoo.eu/contrib/v2/public/submit`

Expected request body: **text/plain** containing JSON.

Why text/plain?
- avoids CORS preflight in most cases (simple request)
- still may require server CORS headers for reading response, but sending works

### Minimal payload fields sent by client
- `type`, `version`, `date`, `title`, `url`, `summary`, `categories`, `author`, `contact`, `license`, `safety`
- `submit`:
  - `kid`: key id
  - `alg`: `ECDSA_P256_SHA256`
  - `sig`: base64url signature over canonical JSON
  - `pow`: optional PoW nonce/proof
  - `origin`: submitting origin (e.g., https://hgpedu.eu)
  - `ts`: unix ms timestamp
  - `pub_spki_b64u`: public key (SPKI) for pure-public experiments

### Server-side verification (ONETOO)
1. Parse JSON, extract `submit`.
2. Rebuild the signed message (canonical JSON with `submit.sig=null` or omitted).
3. Verify signature with the public key referenced by `kid` (or provided in `pub_spki_b64u` for experiments).
4. Verify timestamp window (e.g. +- 5 minutes).
5. If PoW enabled: check difficulty (leading zero bits of SHA-256 over message||"::"||nonce).
6. Apply policy (domain allowlist, safety flags, size limits).
7. Queue as pending / accepted depending on policy.

## Spam/abuse mitigation layers
Client-side:
- per-browser rate limit + cooldown
- PoW
- size cap
- safety wording + human-visible warning

Server-side (recommended):
- IP rate limits
- reject repeated URLs quickly
- ban abusive key ids
- require PoW for anonymous keys
- dynamic difficulty based on load

## UX expectation
- After clicking Submit:
  - "SENT (OPAQUE)" if CORS blocks reading response
  - or "OK/ERROR" if response is readable
- CI ledger sync is the authoritative status.
