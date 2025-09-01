#!/usr/bin/env pwsh
# UwU-CLI Installation Script for PowerShell

Write-Host "Installing UwU-CLI globally..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pip is available
try {
    $pipVersion = pip --version 2>&1
    Write-Host "pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: pip is not available" -ForegroundColor Red
    Write-Host "Please ensure pip is installed with Python" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing UwU-CLI in development mode..." -ForegroundColor Yellow

# Install in development mode
try {
    pip install -e .
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ UwU-CLI installed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "You can now run UwU-CLI from anywhere using:" -ForegroundColor Cyan
        Write-Host "  uwu-cli" -ForegroundColor White
        Write-Host "  uwu" -ForegroundColor White
        Write-Host ""
        Write-Host "To start using it, simply type:" -ForegroundColor Cyan
        Write-Host "  uwu-cli" -ForegroundColor White
        Write-Host ""
        Write-Host "Installation complete!" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Installation failed" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "ERROR: Installation failed: $_" -ForegroundColor Red
    exit 1
}

Read-Host "Press Enter to exit" 