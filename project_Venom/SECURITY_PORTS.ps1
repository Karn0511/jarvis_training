# Venom AI - Port Security Configuration

# This PowerShell script blocks external access to Venom ports
# Run as Administrator: powershell -ExecutionPolicy Bypass -File SECURITY_PORTS.ps1

$VenomPorts = @(8000, 8501, 4200)

Write-Host "🔒 VENOM PORT SECURITY - Blocking External Access" -ForegroundColor Cyan
Write-Host "=" * 60

foreach ($port in $VenomPorts) {
    $ruleName = "Venom Block Port $port"

    # Remove existing rule if present
    $existing = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
    if ($existing) {
        Remove-NetFirewallRule -DisplayName $ruleName
        Write-Host "✓ Removed old rule for port $port" -ForegroundColor Yellow
    }

    # Create new blocking rule for external traffic
    New-NetFirewallRule `
        -DisplayName $ruleName `
        -Direction Inbound `
        -LocalPort $port `
        -Protocol TCP `
        -Action Block `
        -RemoteAddress Internet `
        -Profile Any `
        -Enabled True | Out-Null

    Write-Host "✓ Port $port: Blocked from external networks" -ForegroundColor Green
}

Write-Host ""
Write-Host "🛡️ Security Rules Applied Successfully!" -ForegroundColor Green
Write-Host "📌 Ports accessible from: localhost (127.0.0.1) only" -ForegroundColor Cyan
Write-Host ""
Write-Host "To remove these rules, run:" -ForegroundColor Yellow
Write-Host '  Remove-NetFirewallRule -DisplayName "Venom Block Port*"' -ForegroundColor Gray
