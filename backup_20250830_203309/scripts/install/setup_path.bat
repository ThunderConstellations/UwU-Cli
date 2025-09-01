@echo off
REM UwU-Cli PATH Setup Script for Windows
REM This script adds UwU-Cli to your Windows PATH permanently

echo 🐍 Setting up UwU-Cli in your PATH...

REM Get the current directory (where UwU-Cli is installed)
set "UWU_DIR=%~dp0"
set "UWU_DIR=%UWU_DIR:~0,-1%"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not available in PATH
    echo Please install Python and add it to PATH first
    pause
    exit /b 1
)

REM Check if UwU-CLI files exist
if not exist "%UWU_DIR%\uwu_cli.py" (
    echo ❌ UwU-CLI files not found in current directory
    echo Please run this script from the UwU-CLI installation directory
    pause
    exit /b 1
)

REM Create a global launcher in a system PATH location
set "GLOBAL_LAUNCHER=%USERPROFILE%\AppData\Local\Microsoft\WinGet\Packages\uwu-cli.bat"

REM Create the global launcher script
echo @echo off > "%GLOBAL_LAUNCHER%"
echo REM UwU-CLI Global Launcher >> "%GLOBAL_LAUNCHER%"
echo cd /d "%UWU_DIR%" >> "%GLOBAL_LAUNCHER%"
echo python uwu_cli.py %%* >> "%GLOBAL_LAUNCHER%"

REM Add the directory to user PATH
setx PATH "%PATH%;%UWU_DIR%" >nul 2>&1

REM Also add the global launcher directory to PATH
setx PATH "%PATH%;%USERPROFILE%\AppData\Local\Microsoft\WinGet\Packages" >nul 2>&1

echo ✅ UwU-Cli added to PATH: %UWU_DIR%
echo ✅ Global launcher created: %GLOBAL_LAUNCHER%
echo.
echo 🔄 Please restart your terminal for changes to take effect
echo 🚀 Then you can run 'uwu-cli' from anywhere!
echo.
echo 💡 Alternative commands:
echo    • uwu-cli (global command)
echo    • python uwu_cli.py (from project directory)
echo    • uwu.bat (from project directory)
echo.
pause 