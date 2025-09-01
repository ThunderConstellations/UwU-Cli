@echo off
REM UwU-CLI Direct Installation Script
echo 🚀 Installing UwU-CLI directly from GitHub...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo 📦 Installing UwU-CLI...
pip install git+https://github.com/ThunderConstellations/UwU-Cli.git

if errorlevel 1 (
    echo ❌ Installation failed!
    pause
    exit /b 1
)

echo.
echo ✅ UwU-CLI installed successfully!
echo 🎯 Run with: uwu
echo 🎯 Or: uwu-cli
echo.
echo 🌟 Enjoy your enhanced development shell!
pause
