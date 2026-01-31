"""TFWS v2 probe (GET-only)

Usage:
    from tools.tfws_v2_probe import tfws_v2_check
    ok, meta = tfws_v2_check(target_url)

Contract:
    - Never raises (returns ok=False + error in meta on failure)
    - Timeout is short (default 6s)
    - Success = HTTP 200 + JSON parses to dict
"""

from __future__ import annotations

import json
from urllib.parse import urlparse
import urllib.request
from typing import Dict, Tuple, Any


def tfws_v2_url(target_url: str) -> str:
    """Compute TFWS v2 manifest URL from any absolute target URL."""
    try:
        p = urlparse(target_url)
        if not p.scheme or not p.netloc:
            return ""
        origin = f"{p.scheme}://{p.netloc}"
        return origin.rstrip("/") + "/.well-known/tfws-v2.json"
    except Exception:
        return ""


def tfws_v2_check(target_url: str, timeout: int = 6) -> Tuple[bool, Dict[str, Any]]:
    """GET TFWS v2 JSON (bonus trust signal).

    Returns:
        (ok, meta)
        ok: True if HTTP 200 and JSON body parses to dict/object.
        meta: contains url/http/ok/error
    """
    meta: Dict[str, Any] = {
        "url": None,
        "http": None,
        "ok": False,
        "error": None,
    }

    url = tfws_v2_url(target_url)
    meta["url"] = url

    if not url:
        meta["error"] = "invalid_target_url"
        return False, meta

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "hgpedu-onetoo-sync/2.1"},
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = getattr(resp, "status", 200)
            raw = resp.read()

        meta["http"] = int(code)

        if int(code) != 200:
            meta["error"] = f"http_{code}"
            return False, meta

        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            meta["error"] = "json_not_object"
            return False, meta

        meta["ok"] = True
        return True, meta

    except Exception as e:
        s = str(e) if e is not None else "unknown"
        meta["error"] = s[:160]
        return False, meta
