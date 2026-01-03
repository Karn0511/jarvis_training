#!/usr/bin/env pwsh
# ⚡ VENOM ULTIMATE - Super Fast Launch

Write-Host "`n⚡ VENOM ULTIMATE LAUNCHER ⚡`n" -ForegroundColor Yellow

# Activate venv (workspace root)
$venvPath = "$PSScriptRoot\...\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
}
else {
    Write-Host "⚠️  Virtual environment already active or not found" -ForegroundColor Yellow
}

# Clean old processes
Get-Process | Where-Object { $_.ProcessName -match "python|streamlit" } | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "🔥 Starting services...`n" -ForegroundColor Cyan

# Python executable path
$pythonExe = "$PSScriptRoot\...\.venv\Scripts\python.exe"
$streamlitExe = "$PSScriptRoot\...\.venv\Scripts\streamlit.exe"

# Start everything
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd '$PWD'; & '$pythonExe' venom_daemon.py" -WindowStyle Minimized
Start-Sleep 2

Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd '$PWD'; & '$streamlitExe' run venom_hud.py" -WindowStyle Normal
Start-Sleep 2

Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd '$PWD'; & '$pythonExe' web_server.py" -WindowStyle Normal

Write-Host "✅ VENOM ONLINE`n" -ForegroundColor Green
Write-Host "🌐 HUD:      http://localhost:8501" -ForegroundColor White
Write-Host "🌐 Web API:  http://localhost:8000" -ForegroundColor White
Write-Host "`n💡 Start frontend: cd frontend && npm start`n" -ForegroundColor Cyan
