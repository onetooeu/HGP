# tools/gen-sha256-light.ps1
# Rebuilds .well-known/sha256.json using the EXISTING file list (light scope),
# then signs + verifies with HGPEdu minisign key.

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path ".").Path

$ShaPath  = Join-Path $RepoRoot ".well-known\sha256.json"
$SigPath  = Join-Path $RepoRoot ".well-known\sha256.json.minisig"
$PubKey   = Join-Path $RepoRoot ".well-known\minisign.pub"
$SecKey   = Join-Path $env:USERPROFILE ".minisign-hgpedu\minisign.key"

if (!(Test-Path $ShaPath)) { throw "Missing $ShaPath" }
if (!(Test-Path $PubKey))  { throw "Missing $PubKey" }
if (!(Test-Path $SecKey))  { throw "Missing $SecKey" }

$raw  = Get-Content $ShaPath -Raw
$json = $raw | ConvertFrom-Json

function Get-FileListFromManifest($j) {
  if ($null -ne $j.files) {
    if ($j.files -is [System.Collections.IDictionary]) {
      return @($j.files.Keys)
    }
    if ($j.files -is [System.Array]) {
      $paths = @()
      foreach ($e in $j.files) {
        if ($null -ne $e.path) { $paths += [string]$e.path; continue }
        if ($null -ne $e.file) { $paths += [string]$e.file; continue }
      }
      return $paths
    }
  }

  if ($j -is [System.Array]) {
    $paths = @()
    foreach ($e in $j) {
      if ($null -ne $e.path) { $paths += [string]$e.path; continue }
      if ($null -ne $e.file) { $paths += [string]$e.file; continue }
    }
    return $paths
  }

  throw "Unknown sha256.json structure. Please show first 40 lines of .well-known/sha256.json"
}

function Hash-FileRel($relPath) {
  $rel = $relPath.TrimStart("/").Replace("/", "\")
  $abs = Join-Path $RepoRoot $rel
  if (!(Test-Path $abs)) {
    throw "Manifest references missing file: $relPath (expected at $abs)"
  }
  return (Get-FileHash -Algorithm SHA256 -Path $abs).Hash.ToLowerInvariant()
}

$paths = Get-FileListFromManifest $json
$paths = $paths | Where-Object { $_ -and $_.Trim().Length -gt 0 } | Sort-Object -Unique

Write-Host "Rebuilding sha256.json using existing light scope..."
Write-Host "Files in scope: $($paths.Count)"

if ($null -ne $json.files -and ($json.files -is [System.Collections.IDictionary])) {
  foreach ($p in $paths) { $json.files[$p] = Hash-FileRel $p }
} elseif ($null -ne $json.files -and ($json.files -is [System.Array])) {
  foreach ($e in $json.files) {
    $p = $null
    if ($null -ne $e.path) { $p = [string]$e.path }
    elseif ($null -ne $e.file) { $p = [string]$e.file }
    if ($null -eq $p) { continue }

    $newHash = Hash-FileRel $p
    if ($null -ne $e.sha256) { $e.sha256 = $newHash; continue }
    if ($null -ne $e.hash)   { $e.hash   = $newHash; continue }
    $e | Add-Member -NotePropertyName "sha256" -NotePropertyValue $newHash -Force
  }
} elseif ($json -is [System.Array]) {
  foreach ($e in $json) {
    $p = $null
    if ($null -ne $e.path) { $p = [string]$e.path }
    elseif ($null -ne $e.file) { $p = [string]$e.file }
    if ($null -eq $p) { continue }

    $newHash = Hash-FileRel $p
    if ($null -ne $e.sha256) { $e.sha256 = $newHash; continue }
    if ($null -ne $e.hash)   { $e.hash   = $newHash; continue }
    $e | Add-Member -NotePropertyName "sha256" -NotePropertyValue $newHash -Force
  }
} else {
  throw "Unsupported sha256.json structure."
}

if ($null -ne $json.generated_at) {
  $json.generated_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssK")
}

$out = $json | ConvertTo-Json -Depth 50
Set-Content -Path $ShaPath -Value $out -Encoding utf8

Write-Host "Signing sha256.json with HGPEdu key..."
& minisign.exe -S -s $SecKey -m $ShaPath -x $SigPath | Out-Null

Write-Host "Verifying signature..."
& minisign.exe -V -p $PubKey -m $ShaPath -x $SigPath | Out-Host

Write-Host "✅ Done: rebuilt + signed + verified .well-known/sha256.json"
