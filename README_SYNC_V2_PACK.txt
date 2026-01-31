HGP – ONETOO Sync v2 Pack (read-only)
====================================

What this pack adds
- ONETOO status sync v2 (still GET-only, no tokens, no POST)
- Badge evolution: accepted → verified (UI + ledger)
- Safe issue link builder: works whether ISSUE_BASE contains '?' or not
- VERIFIED added to the status legend (SK/EN)
- .gitignore snippet to ignore Python __pycache__

How to apply (Git Bash)
1) Unzip this pack into the ROOT of your repo (it will place files into tools/, pages/, en/pages/, docs/).
2) Review diff:
   git status
   git diff
3) Run a quick smoke test:
   python tools/onetoo_status_sync.py --dry-run --limit 5
4) Commit + push:
   git add -A
   git commit -m "feat(onetoo): status sync v2 (accepted→verified) + portal badges"
   git pull --rebase
   git push

Notes
- Ledger schema stays compatible: it still writes items[url].status, but now uses:
    status = "verified" instead of "accepted"
  It also stores status_raw for audit (accepted/missing/error).
- Portal UI maps: verified/accepted => VERIFIED badge (green).
