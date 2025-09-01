@echo off
echo Installing UwU-CLI globally...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo.
echo Installing UwU-CLI in development mode...
pip install -e .

if errorlevel 1 (
    echo ERROR: Installation failed
    pause
    exit /b 1
)

echo.
echo ✅ UwU-CLI installed successfully!
echo.
echo You can now run UwU-CLI from anywhere using:
echo   uwu-cli
echo   uwu
echo.
echo To start using it, simply type:
echo   uwu-cli
echo.
echo Installation complete! Press any key to exit...
pause >nul 