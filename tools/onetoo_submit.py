#!/usr/bin/env python3
"""
HGPEdu ↔ ONETOO (read-only)

DEPRECATED ENTRYPOINT (kept for backwards compatibility):
  - tools/onetoo_submit.py

Use instead:
  - tools/onetoo_status_sync.py

Why:
  This project no longer POSTs submissions to ONETOO. It only performs a
  transparent, deterministic, read-only status sync against the public
  ONETOO search endpoint and writes a local ledger.

Mozart mode:
  - no secrets
  - no POST
  - no fake "submit"
"""
from __future__ import annotations

import sys

from onetoo_status_sync import main  # type: ignore


def _notice() -> None:
    msg = (
        "NOTICE: tools/onetoo_submit.py is deprecated. "
        "Use tools/onetoo_status_sync.py instead."
    )
    print(msg, file=sys.stderr)


if __name__ == "__main__":
    _notice()
    raise SystemExit(main())
