# UwU-Cli PATH Setup Script for PowerShell
# This script adds UwU-Cli to your Windows PATH permanently

Write-Host "🐍 Setting up UwU-Cli in your PATH..." -ForegroundColor Green

# Get the current directory (where UwU-Cli is installed)
$uwuDir = $PSScriptRoot

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Python is not available in PATH" -ForegroundColor Red
        Write-Host "Please install Python and add it to PATH first" -ForegroundColor Yellow
        Read-Host "Press Enter to continue"
        exit 1
    }
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not available in PATH" -ForegroundColor Red
    Write-Host "Please install Python and add it to PATH first" -ForegroundColor Yellow
    Read-Host "Press Enter to continue"
    exit 1
}

# Check if UwU-CLI files exist
if (-not (Test-Path "$uwuDir\uwu_cli.py")) {
    Write-Host "❌ UwU-CLI files not found in current directory" -ForegroundColor Red
    Write-Host "Please run this script from the UwU-CLI installation directory" -ForegroundColor Yellow
    Read-Host "Press Enter to continue"
    exit 1
}

# Create a global launcher in a system PATH location
$globalLauncherDir = "$env:USERPROFILE\AppData\Local\Microsoft\WinGet\Packages"
$globalLauncherPath = "$globalLauncherDir\uwu-cli.bat"

# Ensure the directory exists
if (-not (Test-Path $globalLauncherDir)) {
    New-Item -ItemType Directory -Path $globalLauncherDir -Force | Out-Null
}

# Create the global launcher script
$launcherContent = @"
@echo off
REM UwU-CLI Global Launcher
cd /d "$uwuDir"
python uwu_cli.py %*
"@

$launcherContent | Out-File -FilePath $globalLauncherPath -Encoding ASCII

# Add the directory to user PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentPath -notlike "*$uwuDir*") {
    $newPath = "$currentPath;$uwuDir"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "✅ UwU-Cli added to PATH: $uwuDir" -ForegroundColor Green
} else {
    Write-Host "ℹ️  UwU-Cli is already in your PATH" -ForegroundColor Yellow
}

# Also add the global launcher directory to PATH
if ($currentPath -notlike "*$globalLauncherDir*") {
    $newPath = "$currentPath;$globalLauncherDir"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "✅ Global launcher directory added to PATH: $globalLauncherDir" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Global launcher directory is already in your PATH" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Global launcher created: $globalLauncherPath" -ForegroundColor Green
Write-Host "🔄 Please restart your terminal for changes to take effect" -ForegroundColor Cyan
Write-Host "🚀 Then you can run 'uwu-cli' from anywhere!" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Alternative commands:" -ForegroundColor Yellow
Write-Host "   • uwu-cli (global command)" -ForegroundColor White
Write-Host "   • python uwu_cli.py (from project directory)" -ForegroundColor White
Write-Host "   • uwu.bat (from project directory)" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to continue" 