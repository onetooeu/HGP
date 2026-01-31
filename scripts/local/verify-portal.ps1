param(
  [string]$Base = "https://hgpedu.eu"
)

Write-Host "== Portal page ==" -ForegroundColor Cyan
curl.exe -sSI "$Base/pages/portal" | Select-Object -First 20

Write-Host ""
Write-Host "== Portal feed index ==" -ForegroundColor Cyan
curl.exe -sS "$Base/data/portal/index.json" | Select-Object -First 40

Write-Host ""
Write-Host "== Status ledger ==" -ForegroundColor Cyan
curl.exe -sS "$Base/portal/submissions.json" | Select-Object -First 60

Write-Host ""
Write-Host "OK" -ForegroundColor Green
