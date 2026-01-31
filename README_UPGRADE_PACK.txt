# HGP Portal Upgrade Pack (overlay)
Tento ZIP je pripravený ako **overlay** pre existujúci repo `HGP` (hgpedu.eu).
Rozbal ho priamo do koreňa repozitára (prepisuje len pár súborov) a commitni.

## Čo to pridá / zlepší
- ✅ GitHub Issue template pre „Portal submission“ (jednotná štruktúra)
- ✅ PR template (bezpečnostné guardrails)
- ✅ Docs: Mozart mode + význam statusov (ACCEPTED/MISSING/ERROR/PLANNED)
- ✅ Lokálne verify skripty (bash + PowerShell) na rýchlu kontrolu endpointov

## Použitie (Git Bash)
1) Rozbaľ ZIP do koreňa repa
2) `git status`
3) `git add .`
4) `git commit -m "chore(portal): add templates + docs + verify scripts"`
5) `git pull --rebase`
6) `git push`

> Pozn.: Tento pack **nemení** tvoje existujúce portál stránky ani workflow-y, aby to bolo bez rizika.
Ak chceš ďalší pack (v2) s CSS refaktorom a workflow hardeningom, spravíme to ako druhý overlay.
