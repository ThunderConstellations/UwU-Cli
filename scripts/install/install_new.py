#!/usr/bin/env python3
"""
UwU-CLI Installation Script
Simple installation for new users
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        # Check if pip is available
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        
        # Install dependencies
        requirements = [
            "requests>=2.25.1",
            "colorama>=0.4.4",
            "pywin32>=306; sys_platform == 'win32'",
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0"
        ]
        
        for req in requirements:
            print(f"   Installing {req}...")
            subprocess.run([sys.executable, "-m", "pip", "install", req], 
                          capture_output=True, check=True)
        
        print("✅ Dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

def setup_environment():
    """Setup environment variables and paths"""
    print("🔧 Setting up environment...")
    
    try:
        # Get user's home directory
        home_dir = Path.home()
        uwu_dir = home_dir / ".uwu-cli"
        uwu_dir.mkdir(exist_ok=True)
        
        # Create config directory
        config_dir = uwu_dir / "config"
        config_dir.mkdir(exist_ok=True)
        
        # Copy default configs
        if Path("config").exists():
            for config_file in Path("config").glob("*.json"):
                shutil.copy2(config_file, config_dir / config_file.name)
        
        # Create history file
        history_file = uwu_dir / ".uwu_cli_history"
        if not history_file.exists():
            history_file.touch()
        
        print(f"✅ Environment setup in: {uwu_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Environment setup failed: {e}")
        return False

def create_shortcuts():
    """Create shortcuts for easy access"""
    print("🔗 Creating shortcuts...")
    
    try:
        # Get current script location
        script_dir = Path(__file__).parent.absolute()
        uwu_script = script_dir / "uwu_cli.py"
        
        if not uwu_script.exists():
            print("❌ UwU-CLI script not found")
            return False
        
        # Create batch file for Windows
        if sys.platform == "win32":
            batch_file = script_dir / "uwu.bat"
            with open(batch_file, 'w') as f:
                f.write(f'@echo off\npython "{uwu_script}" %*\n')
            print("✅ Created uwu.bat shortcut")
        
        # Create shell script for Unix-like systems
        if sys.platform in ["linux", "darwin"]:
            shell_script = script_dir / "uwu.sh"
            with open(shell_script, 'w') as f:
                f.write(f'#!/bin/bash\npython3 "{uwu_script}" "$@"\n')
            os.chmod(shell_script, 0o755)
            print("✅ Created uwu.sh shortcut")
        
        return True
        
    except Exception as e:
        print(f"❌ Shortcut creation failed: {e}")
        return False

def test_installation():
    """Test if installation was successful"""
    print("🧪 Testing installation...")
    
    try:
        # Try to import UwU-CLI
        sys.path.insert(0, str(Path(__file__).parent))
        import uwu_cli
        
        # Test basic functionality
        cli = uwu_cli.UwUCLI()
        result = cli.builtin_commands(['version'])
        
        if result:
            print("✅ Installation test passed!")
            return True
        else:
            print("❌ Installation test failed")
            return False
            
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def main():
    """Main installation function"""
    print("🚀 UwU-CLI Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed")
        sys.exit(1)
    
    # Create shortcuts
    if not create_shortcuts():
        print("⚠️  Shortcut creation failed, but installation may still work")
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        sys.exit(1)
    
    print("\n🎉 UwU-CLI installed successfully!")
    print("\n💡 Usage:")
    print("   python uwu_cli.py          # Run UwU-CLI")
    print("   python uwu_cli.py --help   # Show help")
    
    if sys.platform == "win32":
        print("   uwu.bat                  # Run with batch file")
    elif sys.platform in ["linux", "darwin"]:
        print("   ./uwu.sh                 # Run with shell script")
    
    print("\n🔧 Configuration:")
    print("   Edit config files in ~/.uwu-cli/config/")
    print("   Set OPENROUTER_API_KEY environment variable for AI features")
    
    print("\n📚 Documentation:")
    print("   https://github.com/UwU-CLI/UwU-Cli")

if __name__ == "__main__":
    main() 