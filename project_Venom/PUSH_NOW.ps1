#!/usr/bin/env powershell
<#
.SYNOPSIS
    One-click push script for Project Venom to GitHub

.DESCRIPTION
    Automatically pushes Project Venom to github.com/Karn0511/jarvis_training
    Handles authentication and verification

.EXAMPLE
    .\PUSH_NOW.ps1
#>

# Enhanced error handling
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  PROJECT VENOM - GITHUB PUSH" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if in correct directory
if (-not (Test-Path ".git")) {
    Write-Host "❌ ERROR: Not in git repository!" -ForegroundColor Red
    Write-Host "Run this script from: E:\Advanced Jarvis\project_Venom" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Git repository detected" -ForegroundColor Green

# Check git status
Write-Host ""
Write-Host "📊 Checking git status..." -ForegroundColor Cyan
$status = git status --porcelain
$commits = git log --oneline -1
Write-Host "Latest commit: $commits" -ForegroundColor Green

# Count commits to push
$unpushed = git log origin/main..HEAD --oneline 2>$null | Measure-Object | Select-Object -ExpandProperty Count
if ($unpushed -gt 0) {
    Write-Host "📤 Commits to push: $unpushed" -ForegroundColor Green
}

# Clear old credentials
Write-Host ""
Write-Host "🔑 Clearing old credentials..." -ForegroundColor Cyan
cmdkey /delete "git:https://github.com" 2>$null | Out-Null
Write-Host "✅ Old credentials cleared" -ForegroundColor Green

# Attempt push
Write-Host ""
Write-Host "⏳ Attempting to push to GitHub..." -ForegroundColor Cyan
Write-Host "  Repository: https://github.com/Karn0511/jarvis_training" -ForegroundColor Yellow
Write-Host ""
Write-Host "📝 When prompted:" -ForegroundColor Yellow
Write-Host "   Username: Karn0511" -ForegroundColor White
Write-Host "   Password: Your GitHub password or Personal Access Token" -ForegroundColor White
Write-Host ""

try {
    # Attempt push with user-friendly output
    git push -u origin main 2>&1 | ForEach-Object {
        if ($_ -match "error|failed|denied") {
            Write-Host "❌ $_" -ForegroundColor Red
        }
        elseif ($_ -match "everything|up-to-date") {
            Write-Host "✅ $_" -ForegroundColor Green
        }
        else {
            Write-Host "✓ $_" -ForegroundColor Green
        }
    }

    $exitCode = $LASTEXITCODE

    if ($exitCode -eq 0) {
        Write-Host ""
        Write-Host "================================" -ForegroundColor Green
        Write-Host "✅ PUSH SUCCESSFUL!" -ForegroundColor Green
        Write-Host "================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "🎉 Your code is now on GitHub!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📍 Next steps:" -ForegroundColor Cyan
        Write-Host "   1. Visit: https://github.com/Karn0511/jarvis_training" -ForegroundColor White
        Write-Host "   2. Verify all 120+ files are visible" -ForegroundColor White
        Write-Host "   3. Check commit history (should show 7 commits)" -ForegroundColor White
        Write-Host "   4. Enable GitHub Actions in Settings" -ForegroundColor White
        Write-Host "   5. Add GEMINI_API_KEY secret (optional)" -ForegroundColor White
        Write-Host ""
        Write-Host "🚀 Ready for production deployment!" -ForegroundColor Green

        # Open GitHub in browser
        Start-Process "https://github.com/Karn0511/jarvis_training"
        Write-Host ""
        Write-Host "Opening GitHub in browser..." -ForegroundColor Cyan
    }
    else {
        Write-Host ""
        Write-Host "❌ Push failed with exit code: $exitCode" -ForegroundColor Red
        Write-Host ""
        Write-Host "Troubleshooting:" -ForegroundColor Yellow
        Write-Host "  • Check your GitHub credentials (Karn0511)" -ForegroundColor White
        Write-Host "  • Verify PAT token has 'repo' and 'workflow' scopes" -ForegroundColor White
        Write-Host "  • Try again: .\PUSH_NOW.ps1" -ForegroundColor White
        exit 1
    }

}
catch {
    Write-Host ""
    Write-Host "❌ Error during push: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Script completed successfully!" -ForegroundColor Green
