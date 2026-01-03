#!/usr/bin/env powershell
<#
.SYNOPSIS
    GitHub login and push helper script

.DESCRIPTION
    Logs you into GitHub as Karn0511 and then pushes your code
#>

Write-Host "================================" -ForegroundColor Green
Write-Host "  GITHUB LOGIN & PUSH" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Step 1: Login to GitHub
Write-Host "📝 STEP 1: Login to GitHub" -ForegroundColor Yellow
Write-Host "Running: gh auth login" -ForegroundColor Cyan
Write-Host ""
Write-Host "When prompted:" -ForegroundColor Yellow
Write-Host "  • What account do you want to log into? → GitHub.com" -ForegroundColor White
Write-Host "  • What is your preferred protocol? → HTTPS" -ForegroundColor White
Write-Host "  • Authenticate Git with your credentials? → Y" -ForegroundColor White
Write-Host "  • How would you like to authenticate? → Paste an authentication token (or use browser)" -ForegroundColor White
Write-Host ""

gh auth login

Write-Host ""
Write-Host "✅ GitHub auth configured" -ForegroundColor Green

# Verify login
$authStatus = gh auth status 2>&1
if ($authStatus -match "Karn0511") {
    Write-Host "✅ Logged in as Karn0511" -ForegroundColor Green
}
else {
    Write-Host "⚠️  Auth status: $authStatus" -ForegroundColor Yellow
}

# Step 2: Push code
Write-Host ""
Write-Host "📤 STEP 2: Pushing code to GitHub..." -ForegroundColor Yellow
Write-Host ""

cd "E:\Advanced Jarvis\project_Venom"
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "✅ SUCCESS! CODE PUSHED!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 Your Project Venom is now on GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📍 Visit: https://github.com/Karn0511/jarvis_training" -ForegroundColor Cyan
    Write-Host ""
    Start-Process "https://github.com/Karn0511/jarvis_training"
}
else {
    Write-Host ""
    Write-Host "❌ Push failed!" -ForegroundColor Red
    Write-Host "Check the error above and try again." -ForegroundColor Yellow
}
