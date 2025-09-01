#!/usr/bin/env python3
"""
Free Distribution Helper for UwU-CLI
Provides multiple free ways to distribute UwU-CLI without PyPI account
"""

import os
import shutil
import subprocess
import zipfile
from pathlib import Path

def create_github_release_package():
    """Create a package ready for GitHub Releases"""
    print("🚀 Creating GitHub Release Package...")
    
    # Ensure we're in the right directory
    if not Path("secure_dist").exists():
        print("❌ secure_dist directory not found!")
        return False
    
    # Create release directory
    release_dir = Path("github_release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # Copy secure distribution
    shutil.copytree("secure_dist", release_dir / "uwu-cli-2.0.0")
    
    # Create installation instructions
    install_instructions = """# 🚀 UwU-CLI v2.0.0 Installation

## Quick Install (Recommended)
```bash
pip install https://github.com/ThunderConstellations/UwU-Cli/releases/download/v2.0.0/uwu_cli-2.0.0-py3-none-any.whl
```

## Manual Install
1. Download the wheel file (.whl)
2. Install with: `pip install uwu_cli-2.0.0-py3-none-any.whl`
3. Run with: `uwu` or `uwu-cli`

## Features
- Professional development shell
- AI assistance integration
- Multi-shell support (CMD, PowerShell, Bash)
- Enhanced quick commands
- Cursor IDE integration
- Telegram remote control
- Cross-platform compatibility

## Support
- GitHub: https://github.com/ThunderConstellations/UwU-Cli
- Issues: https://github.com/ThunderConstellations/UwU-Cli/issues
"""
    
    with open(release_dir / "INSTALL.md", "w", encoding="utf-8") as f:
        f.write(install_instructions)
    
    # Create ZIP package
    zip_path = release_dir / "uwu-cli-2.0.0-github-release.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir / "uwu-cli-2.0.0"):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(release_dir)
                zipf.write(file_path, arcname)
    
    print(f"✅ GitHub Release package created: {zip_path}")
    return True

def create_direct_install_script():
    """Create a script for direct GitHub installation"""
    print("🔗 Creating Direct Install Script...")
    
    script_content = """@echo off
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
"""
    
    with open("install_uwu_cli.bat", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    # Create PowerShell version
    ps_script_content = """# UwU-CLI Direct Installation Script (PowerShell)
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
"""
    
    with open("install_uwu_cli.ps1", "w", encoding="utf-8") as f:
        f.write(ps_script_content)
    
    print("✅ Direct install scripts created:")
    print("   - install_uwu_cli.bat (Windows CMD)")
    print("   - install_uwu_cli.ps1 (PowerShell)")
    return True

def show_distribution_options():
    """Show all available distribution options"""
    print("\n" + "="*60)
    print("🚀 UwU-CLI Distribution Options")
    print("="*60)
    
    print("\n📦 **Option 1: GitHub Releases (Recommended - Completely Free)**")
    print("   1. Run: python free_distribution.py --github")
    print("   2. Upload the created package to GitHub Releases")
    print("   3. Users install with: pip install <release-url>")
    
    print("\n🔗 **Option 2: Direct GitHub Installation (Free)**")
    print("   1. Run: python free_distribution.py --direct")
    print("   2. Users install with: pip install git+<repo-url>")
    
    print("\n🌐 **Option 3: Manual Distribution (Free)**")
    print("   1. Share the secure_dist/ folder")
    print("   2. Users install with: pip install -e <folder-path>")
    
    print("\n💡 **Pro Tip**: GitHub Releases is the most professional option!")
    print("   It provides versioned releases and easy installation URLs.")

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--github":
            create_github_release_package()
        elif sys.argv[1] == "--direct":
            create_direct_install_script()
        else:
            print("❌ Unknown option. Use --github or --direct")
    else:
        show_distribution_options()
        
        print("\n🎯 **Quick Start Commands:**")
        print("   python free_distribution.py --github    # Create GitHub release package")
        print("   python free_distribution.py --direct    # Create direct install scripts")

if __name__ == "__main__":
    main() 