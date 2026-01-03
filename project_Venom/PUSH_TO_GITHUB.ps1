#!/usr/bin/env powershell
# 🚀 Venom AI - GitHub Push Script
# Push Project Venom to your GitHub repository

Write-Host "╔════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         🚀 PROJECT VENOM - GitHub Push Script                        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configuration
$GITHUB_USER = "Karn0511"
$REPO_NAME = "jarvis_training"
$REPO_URL = "https://github.com/$GITHUB_USER/$REPO_NAME.git"

Write-Host "📦 Repository: $REPO_URL" -ForegroundColor Yellow
Write-Host ""

# Step 1: Verify Git Status
Write-Host "Step 1️⃣  : Checking Git Status..." -ForegroundColor Green
cd (Split-Path -Parent $PSCommandPath)
git status

Write-Host ""
Write-Host "Step 2️⃣  : Setting Remote URL..." -ForegroundColor Green
git remote remove origin 2>$null
git remote add origin $REPO_URL
Write-Host "✅ Remote set to: $REPO_URL" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3️⃣  : Attempting Push..." -ForegroundColor Green
Write-Host "Note: You may be prompted for GitHub credentials" -ForegroundColor Yellow
Write-Host ""

# Step 2: Push
git push -u origin main --force 2>&1 | Tee-Object -Variable pushOutput

# Check result
if ($pushOutput -match "fatal" -or $LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Push failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting steps:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://github.com/settings/tokens" -ForegroundColor Gray
    Write-Host "2. Create a Personal Access Token (repo scope)" -ForegroundColor Gray
    Write-Host "3. Run: git push https://<token>@github.com/$GITHUB_USER/$REPO_NAME.git main" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✅ Push successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Repository Status:" -ForegroundColor Cyan
    Write-Host "   URL: $REPO_URL" -ForegroundColor White
    Write-Host "   Branch: main" -ForegroundColor White
    
    # Show commit info
    Write-Host ""
    Write-Host "📝 Latest Commits:" -ForegroundColor Cyan
    git log --oneline -5
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Script completed!" -ForegroundColor Green
