@echo off
REM UwU-CLI Windows Installer
REM Usage: installer.bat

echo ╔════════════════════════════════════════════╗
echo ║      ✨ UwU-CLI Windows Installer ✨        ║
echo ╚════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo ✅ Python detected

REM Install dependencies
echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Create installation directory
set INSTALL_DIR=%USERPROFILE%\.uwu-cli
echo.
echo 📁 Creating installation directory: %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
echo 📋 Copying UwU-CLI files...
xcopy /E /I /Y * "%INSTALL_DIR%"

REM Create launcher batch file
echo 🔗 Creating launcher script...
echo @echo off > "%INSTALL_DIR%\uwu.bat"
echo python "%USERPROFILE%\.uwu-cli\uwu_cli.py" %%* >> "%INSTALL_DIR%\uwu.bat"

REM Create PowerShell launcher
echo 🔗 Creating PowerShell launcher...
echo python "$env:USERPROFILE\.uwu-cli\uwu_cli.py" $args > "%INSTALL_DIR%\uwu.ps1"

REM Add to PATH (Windows)
echo 🛤️  Adding to Windows PATH...
setx PATH "%PATH%;%INSTALL_DIR%"

REM Create configuration
echo ⚙️  Creating default configuration...
if not exist "%INSTALL_DIR%\config" mkdir "%INSTALL_DIR%\config"

echo { > "%INSTALL_DIR%\config\default_config.json"
echo   "prompt_style": "uwu", >> "%INSTALL_DIR%\config\default_config.json"
echo   "enable_telemetry": false, >> "%INSTALL_DIR%\config\default_config.json"
echo   "phrase_pack": "default", >> "%INSTALL_DIR%\config\default_config.json"
echo   "auto_save_every": 10, >> "%INSTALL_DIR%\config\default_config.json"
echo   "max_history": 500, >> "%INSTALL_DIR%\config\default_config.json"
echo   "safe_mode": false, >> "%INSTALL_DIR%\config\default_config.json"
echo   "theme_colors": true, >> "%INSTALL_DIR%\config\default_config.json"
echo   "ascii_effects": true, >> "%INSTALL_DIR%\config\default_config.json"
echo   "sound_enabled": false, >> "%INSTALL_DIR%\config\default_config.json"
echo   "plugins_enabled": true, >> "%INSTALL_DIR%\config\default_config.json"
echo   "ai_enabled": true, >> "%INSTALL_DIR%\config\default_config.json"
echo   "default_ai_model": "gpt-4o-mini" >> "%INSTALL_DIR%\config\default_config.json"
echo } >> "%INSTALL_DIR%\config\default_config.json"

REM Create AI configuration
echo 🤖 Creating AI configuration...
echo { > "%INSTALL_DIR%\ai_config.json"
echo   "openrouter_api_key": "", >> "%INSTALL_DIR%\ai_config.json"
echo   "use_local_llm": false, >> "%INSTALL_DIR%\ai_config.json"
echo   "local_llm_cmd": "", >> "%INSTALL_DIR%\ai_config.json"
echo   "model": "gpt-4o-mini", >> "%INSTALL_DIR%\ai_config.json"
echo   "timeout_seconds": 30, >> "%INSTALL_DIR%\ai_config.json"
echo   "max_tokens": 300, >> "%INSTALL_DIR%\ai_config.json"
echo   "temperature": 0.9 >> "%INSTALL_DIR%\ai_config.json"
echo } >> "%INSTALL_DIR%\ai_config.json"

echo.
echo 🎉 UwU-CLI installation complete!
echo.
echo 🚀 To start UwU-CLI, run:
echo    uwu
echo.
echo 📁 Installation directory: %INSTALL_DIR%
echo ⚙️  Configuration: %INSTALL_DIR%\config\
echo 🔌 Plugins: %INSTALL_DIR%\plugins\
echo.
echo 💡 For AI features, set your OpenRouter API key:
echo    set OPENROUTER_API_KEY=your-key-here
echo.
echo 🔄 Restart your terminal for PATH changes to take effect
echo.
echo UwU~ Stay chaotic, stay sparkly! ✨
pause 