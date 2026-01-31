# HGPEdu Portal Autopilot – reálne funkčné zapojenie (GitHub Actions)

Tento repozitár je statický portál. „Autopilot“ znamená automatizované **schvaľovanie príspevkov** cez GitHub Issues
a následné publikovanie do statického feedu, ktorý sa zobrazuje na:

- `https://hgpedu.eu/pages/portal.html` (front-end)
- `data/portal/index.json` (statický feed)

## 1) Workflow dnes (plne funkčné)

1. Niekto vytvorí GitHub Issue s názvom začínajúcim na **`[PORTAL]`** (ideálne cez Issue template).
2. GitHub Actions spustí **Portal Autopilot**:
   - vytiahne JSON payload z Issue
   - striktne ho overí (HTTPS, povinné polia, limity)
   - zapíše audit log (`data/portal/entries.jsonl`)
   - publikuje do `data/portal/index.json`
   - zapíše rozhodnutie do `data/portal/decisions/<issue>.json`
3. Autopilot spraví commit + push do `main`.
4. Statický web (Pages/Cloudflare Pages) sa po novom commite obnoví.

## 2) TFWS verifikovateľné artefakty (sha256/minisign)

Repo už obsahuje:
- `.well-known/sha256.json`
- `.well-known/sha256.json.minisig`
- `.well-known/minisign.pub`

Autopilot workflow vie **automaticky** aktualizovať `.well-known/sha256.json`
a (ak nastavíš secrets) aj **podpísať** novú verziu.

### Nastav v GitHub Secrets:
- `MINISIGN_SECRET_KEY` – obsah súkromného kľúča (napr. súbor `minisign.key` ako text)
- `MINISIGN_PASSPHRASE` – passphrase kľúča (ak je nastavená)

Potom Autopilot po každom publish:
- prepočíta `.well-known/sha256.json`
- vytvorí/obnoví `.well-known/sha256.json.minisig`

> Bez týchto secrets bude portál stále fungovať, len sa podpis nebude automaticky obnovovať.

## 3) ONETOO integrácia (submit do AI Search)

Workflow **ONETOO Submit Autopilot** beží:
- pri push do `data/portal/index.json` / `data/portal/entries.jsonl`
- a tiež plánovane (cron)

Aby reálne submitoval záznamy, nastav secrets:
- `ONETOO_TOKEN` – token (ak endpoint vyžaduje autentifikáciu)
- `ONETOO_SUBMIT_ENDPOINT` – napr. `https://search.onetoo.eu/contrib/v2/submit`

Skript: `tools/onetoo_submit.py`

## 4) Lokálny test

Bez GitHub Actions si vieš otestovať validáciu takto:

```bash
export BODY='```json
{"type":"hgp.portal.submission","version":"2.0","date":"2026-01-10","title":"Claude (Anthropic)","url":"https://claude.ai","summary":"Constitutional AI assistant by Anthropic","categories":["AI","Assistant","Research"]}
```'
python tools/portal_autopilot.py --issue 9999
```

Potom skontroluj:
- `data/portal/index.json` (nový item)
- `data/portal/entries.jsonl` (audit)
- `data/portal/decisions/9999.json` (decision)

