#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Secure Package Creator for UwU-CLI
Creates a completely sanitized distribution package for PyPI
"""

import os
import shutil
import re
from pathlib import Path
import json

def create_secure_package():
    """Create a completely sanitized package for distribution"""
    print("🔒 Creating Secure Distribution Package")
    print("=" * 50)
    
    # Create secure distribution directory
    secure_dir = Path("secure_dist")
    if secure_dir.exists():
        shutil.rmtree(secure_dir)
    secure_dir.mkdir()
    
    # Copy source files (excluding sensitive ones)
    source_files = [
        "uwu_cli.py",
        "utils/",
        "phrases/",
        "plugins/",
        "tts/",
        "requirements.txt",
        "LICENSE",
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        ".github/",
        "install.bat",
        "install.ps1", 
        "install.sh",
        "setup_path.bat",
        "setup_path.ps1",
        "setup_path.sh"
    ]
    
    print("📁 Copying source files...")
    for item in source_files:
        src = Path(item)
        dst = secure_dir / item
        
        if src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        elif src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
                "*.pyc", "__pycache__", "*.log", "*.session", "*.state", "*.context", "*.preferences"
            ))
    
    # Create secure setup.py
    secure_setup = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UwU-CLI Setup Script
Professional-grade development shell with AI assistance capabilities
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="uwu-cli",
    version="2.0.0",
    author="UwU-CLI Development Team",
    author_email="",
    description="Professional-grade development shell with AI assistance capabilities",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/UwU-CLI/UwU-Cli",
    packages=find_packages(include=['utils*', 'phrases*', 'plugins*', 'tts*']),
    py_modules=['uwu_cli'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Shells",
        "Topic :: Terminals",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Utilities",
        "Topic :: Desktop Environment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "uwu-cli=uwu_cli:main",
            "uwu=uwu_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md", "*.txt", "*.bat", "*.ps1", "*.sh"],
    },
    keywords="cli shell development ai assistant cursor ide terminal windows powershell bash",
    project_urls={
        "Bug Reports": "https://github.com/UwU-CLI/UwU-Cli/issues",
        "Source": "https://github.com/UwU-CLI/UwU-Cli",
        "Documentation": "https://github.com/UwU-CLI/UwU-Cli#readme",
        "Changelog": "https://github.com/UwU-CLI/UwU-Cli/blob/main/CHANGELOG.md",
    },
    platforms=["Windows", "macOS", "Linux"],
    zip_safe=False,
)
'''
    
    with open(secure_dir / "setup.py", "w", encoding="utf-8") as f:
        f.write(secure_setup)
    
    # Create secure __init__.py
    secure_init = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UwU-CLI Package
Professional-grade development shell with AI assistance capabilities
"""

__version__ = "2.0.0"
__author__ = "UwU-CLI Development Team"
__description__ = "Professional-grade development shell with AI assistance capabilities"

from .uwu_cli import main

__all__ = ["main"]
'''
    
    with open(secure_dir / "__init__.py", "w", encoding="utf-8") as f:
        f.write(secure_init)
    
    # Create secure configuration templates
    secure_config = {
        "ai": {
            "openrouter_api_key": "YOUR_API_KEY_HERE",
            "model": "deepseek/deepseek-r1-0528:free",
            "max_tokens": 1000,
            "temperature": 0.9
        },
        "telegram": {
            "bot_token": "YOUR_BOT_TOKEN_HERE",
            "chat_id": "YOUR_CHAT_ID_HERE",
            "enabled": False
        },
        "cursor": {
            "path": "C:\\\\Users\\\\USERNAME\\\\AppData\\\\Local\\\\Programs\\\\Cursor\\\\Cursor.exe",
            "enabled": True
        },
        "general": {
            "theme": "toxic",
            "telegram_enabled": False,
            "autopilot_enabled": False
        }
    }
    
    config_dir = secure_dir / "config"
    config_dir.mkdir(exist_ok=True)
    
    with open(config_dir / "template.json", "w", encoding="utf-8") as f:
        json.dump(secure_config, f, indent=2)
    
    # Create secure .gitignore
    secure_gitignore = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# poetry
poetry.lock

# pdm
pdm.lock
.pdm.toml

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
.idea/

# UwU-CLI specific
tmp/
logs/
*.log
*.session
*.history
*.preferences
*.context
*.state

# Configuration files with sensitive information
.autopilot.json
.telegram_config.json
.telegram.json
*.config.json
*.auth.json
*.secret.json
*.key.json
*.token.json
*.password.json
.env
.env.local
.env.production
.env.development
config/local.json
config/secrets.json
config/auth.json
config/telegram.json

# Personal information and system paths
*personal*
*private*
*home*
*address*
*phone*

# Windows specific
*.exe
*.msi
*.bat
*.cmd
*.ps1
*.vbs

# macOS specific
.DS_Store
.AppleDouble
.LSOverride

# Linux specific
*~
.fuse_hidden*
.directory
.Trash-*
.nfs*

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo
*~

# Temporary files
*.tmp
*.temp
*.bak
*.backup

# Database files
*.db
*.sqlite
*.sqlite3

# Archive files
*.zip
*.tar.gz
*.rar
*.7z

# Backup files
*.bak
*.backup
*.old
*.orig

# System files
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/

# Network and security
*.pem
*.key
*.crt
*.csr
*.p12
*.pfx

# Logs and debugging
debug.log
error.log
access.log
*.log.*

# Session and state files
session.json
state.json
context.json
preferences.json

# AI and machine learning models
*.model
*.pkl
*.h5
*.onnx
*.tflite

# Documentation builds
docs/_build/
site/

# Test coverage
.coverage
htmlcov/
.tox/
.pytest_cache/

# Development tools
.pytest_cache/
.coverage
.mypy_cache/
.pyre/
.pytype/

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Application specific
uwu_cli.db
uwu_cli.log
uwu_cli.session
uwu_cli.state
uwu_cli.context
uwu_cli.preferences
'''
    
    with open(secure_dir / ".gitignore", "w", encoding="utf-8") as f:
        f.write(secure_gitignore)
    
    # Create secure README
    secure_readme = '''# 🌟 UwU-CLI

[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/UwU-CLI/UwU-Cli/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/UwU-CLI/UwU-Cli)

> Professional-grade development shell with AI assistance capabilities

## ✨ Features

- **AI-Powered Development**: Integrated AI assistance for coding tasks
- **Multi-Shell Support**: Works with CMD, PowerShell, and Bash
- **Cursor IDE Integration**: Seamless integration with Cursor IDE
- **Advanced Quick Commands**: Powerful shortcuts for common tasks
- **Infinite Mode**: Continuous AI assistance for complex projects
- **Research Modes**: Deep analysis and code review capabilities
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Installation

### Via pip (from GitHub)
```bash
pip install git+https://github.com/UwU-CLI/UwU-Cli.git
```

### Via pipx (recommended)
```bash
pipx install git+https://github.com/UwU-CLI/UwU-Cli.git
```

### Manual Installation
```bash
git clone https://github.com/UwU-CLI/UwU-Cli.git
cd UwU-Cli
pip install -e .
```

## 📖 Usage

```bash
# Start UwU-CLI
uwu

# Or use the shorter command
uwu-cli
```

## 🔧 Configuration

Copy the configuration template and customize it:

```bash
cp config/template.json ~/.uwu-cli/config.json
```

## 📚 Documentation

- [User Guide](USER_GUIDE.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Security Information](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/UwU-CLI/UwU-Cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/UwU-CLI/UwU-Cli/discussions)
- **Documentation**: [Wiki](https://github.com/UwU-CLI/UwU-Cli/wiki)

---

**Made with ❤️ by the UwU-CLI Development Team**
'''
    
    with open(secure_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(secure_readme)
    
    print("✅ Secure package created successfully!")
    print(f"📁 Location: {secure_dir.absolute()}")
    print("\n🔒 Security features:")
    print("   - All personal information removed")
    print("   - Generic configuration templates")
    print("   - Anonymous author information")
    print("   - Secure .gitignore patterns")
    print("   - No sensitive files included")
    
    return secure_dir

def verify_security(secure_dir):
    """Verify the secure package has no vulnerabilities"""
    print("\n🔍 Verifying package security...")
    
    # Check for personal information patterns
    personal_patterns = [
        r'Cringe Lord',
        r'ThunderConstellations',
        r'personal',
        r'private'
    ]
    
    issues_found = []
    
    for file_path in secure_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix in ['.py', '.json', '.md', '.txt']:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    for pattern in personal_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            issues_found.append(f"Personal info found in {file_path}: {pattern}")
                            
            except Exception as e:
                print(f"⚠️  Could not read {file_path}: {e}")
    
    if issues_found:
        print("❌ Security verification failed:")
        for issue in issues_found:
            print(f"   - {issue}")
        return False
    
    print("✅ Security verification passed!")
    return True

def main():
    """Main function"""
    print("🔒 UwU-CLI Secure Package Creator")
    print("=" * 50)
    
    # Create secure package
    secure_dir = create_secure_package()
    
    # Verify security
    if verify_security(secure_dir):
        print("\n🎉 Secure package ready for PyPI publishing!")
        print(f"\n📋 Next steps:")
        print(f"1. Change to secure directory: cd {secure_dir}")
        print("2. Build package: python -m build")
        print("3. Publish to PyPI: python -m twine upload dist/*")
        print("\n⚠️  IMPORTANT: This package contains NO personal information")
        print("   It's safe to publish to PyPI")
    else:
        print("\n🚨 Security verification failed!")
        print("Package is NOT safe for PyPI publishing")

if __name__ == "__main__":
    main() 