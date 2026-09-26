# run_scan.ps1
# Member 4 Security deliverable — ForgeBridge / AUTOFACTORY-2005
#
# Runs Semgrep against the legacy C source and writes JSON results to
# security/semgrep-results.json.
#
# Usage (from repository root):
#   .\security\run_scan.ps1
#
# Prerequisites:
#   semgrep must be installed and on the PATH.
#   Install: pip install semgrep
#
# Exit codes match Semgrep's own exit codes:
#   0  — scan completed, no findings
#   1  — scan completed, findings present
#   2  — scan error

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ── Paths ────────────────────────────────────────────────────────────────────

$repoRoot   = Split-Path -Parent $PSScriptRoot
$scanTarget = Join-Path $repoRoot 'legacy\AUTOFACTORY-2005\src'
$outputFile = Join-Path $PSScriptRoot 'semgrep-results.json'

# ── Pre-flight checks ────────────────────────────────────────────────────────

if (-not (Get-Command semgrep -ErrorAction SilentlyContinue)) {
    Write-Error "semgrep is not on the PATH. Install with: pip install semgrep"
    exit 2
}

if (-not (Test-Path $scanTarget)) {
    Write-Error "Scan target not found: $scanTarget"
    exit 2
}

# ── Run Semgrep ──────────────────────────────────────────────────────────────

Write-Host "Scan target : $scanTarget"
Write-Host "Rule set    : p/c"
Write-Host "Output file : $outputFile"
Write-Host ""
Write-Host "Running Semgrep..."

semgrep `
    --config p/c `
    --json `
    --output "$outputFile" `
    --no-git-ignore `
    --metrics=off `
    "$scanTarget"

$semgrepExit = $LASTEXITCODE

# ── Report ───────────────────────────────────────────────────────────────────

if ($semgrepExit -eq 0) {
    Write-Host "Semgrep completed — no findings."
} elseif ($semgrepExit -eq 1) {
    Write-Host "Semgrep completed — findings written to: $outputFile"
    Write-Host "Review semgrep-results.json for raw scanner output."
    Write-Host "Any interpretation of findings must cite rule ID, file path, and line number."
} else {
    Write-Error "Semgrep exited with error code $semgrepExit. Check the output above."
}

exit $semgrepExit
