# Reseal after update (minisign)

This update changes site content and regenerates `.well-known/sha256.json`.
That means the existing `.minisig` files for `sha256.json` are now **outdated** and must be re-signed on your machine.

## 1) Regenerate sha256 manifest (deterministic)
From repo root:

```bash
python3 tools/gen_sha256_json.py \
  --include onetoo/services.json \
  --include .well-known/onetoo-services.json
```

This updates:
- `.well-known/sha256.json`
- and (in this bundle) `_verify/sha256.json` is already copied from it, but you can re-copy if you want:
```bash
cp .well-known/sha256.json _verify/sha256.json
```

## 2) Re-sign the updated manifest
Replace `PATH_TO_SECRET_KEY` with your minisign secret key path.

```bash
minisign -S -s PATH_TO_SECRET_KEY -m .well-known/sha256.json -x .well-known/sha256.json.minisig
minisign -S -s PATH_TO_SECRET_KEY -m _verify/sha256.json -x _verify/sha256.json.minisig
```

## 3) Quick verify
```bash
curl -fsSL https://hgpedu.eu/.well-known/minisign.pub -o /tmp/minisign.pub
minisign -V -p /tmp/minisign.pub -m .well-known/sha256.json -x .well-known/sha256.json.minisig
```

If you publish `_verify/` as well:
```bash
minisign -V -p /tmp/minisign.pub -m _verify/sha256.json -x _verify/sha256.json.minisig
```
