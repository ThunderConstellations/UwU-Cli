# UwU-CLI Direct Installation Script (PowerShell)
Write-Host "🚀 Installing UwU-CLI directly from GitHub..." -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    python --version | Out-Null
} catch {
    Write-Host "❌ Python not found! Please install Python 3.8+ first." -ForegroundColor Red
    Read-Host "Press Enter to continue"
    exit 1
}

Write-Host "📦 Installing UwU-CLI..." -ForegroundColor Yellow
pip install git+https://github.com/ThunderConstellations/UwU-Cli.git

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Installation failed!" -ForegroundColor Red
    Read-Host "Press Enter to continue"
    exit 1
}

Write-Host ""
Write-Host "✅ UwU-CLI installed successfully!" -ForegroundColor Green
Write-Host "🎯 Run with: uwu" -ForegroundColor Cyan
Write-Host "🎯 Or: uwu-cli" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌟 Enjoy your enhanced development shell!" -ForegroundColor Magenta
Read-Host "Press Enter to continue"
