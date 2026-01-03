#!/usr/bin/env pwsh
<#
.SYNOPSIS
    🚀 VENOM Ultimate Launch Script - One-Click Startup
.DESCRIPTION
    Launches all Venom components with the new glass morphism UI
.EXAMPLE
    .\LAUNCH_VENOM.ps1
#>

$ErrorActionPreference = "Stop"

# Banner
Write-Host "=" -ForegroundColor Cyan -NoNewline; Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "⚡ VENOM ULTIMATE LAUNCHER ⚡" -ForegroundColor Yellow
Write-Host "=" -ForegroundColor Cyan -NoNewline; Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host ""

# Check if in correct directory
if (-not (Test-Path "main.py")) {
    Write-Host "❌ Error: Run this script from project_Venom directory" -ForegroundColor Red
    exit 1
}

# Check virtual environment
$venvPath = "$PSScriptRoot\...\.venv\Scripts\Activate.ps1"
if (-not (Test-Path $venvPath)) {
    Write-Host "❌ Error: Virtual environment not found at workspace root." -ForegroundColor Red
    Write-Host "Expected: e:\Advanced Jarvis\.venv" -ForegroundColor Yellow
    exit 1
}

Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
& $venvPath

Write-Host "✅ Environment activated" -ForegroundColor Green
Write-Host ""

Write-Host "🎯 Starting Venom Services..." -ForegroundColor Yellow
Write-Host ""

# Kill any existing processes
Write-Host "🧹 Cleaning up old processes..." -ForegroundColor Cyan
Get-Process | Where-Object { $_.ProcessName -match "python|streamlit" } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Python paths
$pythonExe = "$PSScriptRoot\...\.venv\Scripts\python.exe"
$streamlitExe = "$PSScriptRoot\...\.venv\Scripts\streamlit.exe"

# Start Daemon (Background)
Write-Host "🔥 Launching Immortality Daemon..." -ForegroundColor Magenta
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd '$PWD'; & '$pythonExe' venom_daemon.py" -WindowStyle Minimized

Start-Sleep -Seconds 2

# Start HUD (Background)
Write-Host "👁️  Launching HUD Dashboard..." -ForegroundColor Cyan
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd '$PWD'; & '$streamlitExe' run venom_hud.py --server.headless true" -WindowStyle Normal

Start-Sleep -Seconds 3

# Start Web Server (Background)
Write-Host "🌐 Launching Web Server..." -ForegroundColor Blue
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd '$PWD'; & '$pythonExe' web_server.py" -WindowStyle Normal

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "=" -ForegroundColor Green -NoNewline; Write-Host ("=" * 79) -ForegroundColor Green
Write-Host "✅ VENOM FULLY OPERATIONAL" -ForegroundColor Green
Write-Host "=" -ForegroundColor Green -NoNewline; Write-Host ("=" * 79) -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Services Running:" -ForegroundColor Yellow
Write-Host "   • Daemon (Auto-Restart):    Port N/A" -ForegroundColor White
Write-Host "   • HUD Dashboard:            http://localhost:8501" -ForegroundColor White
Write-Host "   • Web API:                  http://localhost:8000" -ForegroundColor White
Write-Host "   • Frontend UI:              http://localhost:4200" -ForegroundColor White
Write-Host ""
Write-Host "💡 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Open HUD:     http://localhost:8501" -ForegroundColor Gray
Write-Host "   2. Open Frontend: cd frontend && npm start" -ForegroundColor Gray
Write-Host "   3. Monitor logs in the daemon window" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C in daemon window to shutdown all services" -ForegroundColor Yellow
Write-Host ""
