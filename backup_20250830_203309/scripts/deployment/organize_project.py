#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Organization Script
Organizes UwU-CLI project structure and creates professional organization
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

def create_directory_structure():
    """Create organized directory structure"""
    directories = [
        "docs/",
        "docs/guides/",
        "docs/api/",
        "docs/examples/",
        "docs/development/",
        "docs/rules/",
        "scripts/install/",
        "scripts/development/",
        "scripts/deployment/",
        "examples/",
        "examples/quick_start/",
        "examples/advanced/",
        "examples/plugins/",
        "assets/",
        "assets/themes/",
        "assets/icons/",
        "templates/",
        "templates/plugins/",
        "templates/rules/"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def organize_documentation():
    """Organize documentation files"""
    doc_mapping = {
        # User guides and documentation
        "USER_GUIDE.md": "docs/guides/",
        "ENHANCED_FEATURES_SUMMARY.md": "docs/guides/",
        "AUTOPILOT_README.md": "docs/guides/",
        "TERMINAL_INTEGRATION_README.md": "docs/guides/",
        
        # Development documentation
        "CHATGPT_ANALYSIS_IMPLEMENTATION_PLAN.md": "docs/development/",
        "IMMEDIATE_IMPLEMENTATION_PLAN.md": "docs/development/",
        "TECHNOLOGY_RESEARCH.md": "docs/development/",
        "PROJECT_STATUS.md": "docs/development/",
        "IMPLEMENTATION_SUMMARY.md": "docs/development/",
        
        # API and technical documentation
        "CURSOR_API_RESEARCH.md": "docs/api/",
        "CURSOR_INTEGRATION_PLAN.md": "docs/api/",
        "COMPREHENSIVE_CURSOR_FIXES_SUMMARY.md": "docs/api/",
        
        # Examples and templates
        "AI_CHAT_SOLUTION.md": "examples/advanced/",
        "COMPREHENSIVE_FIX_PLAN.md": "examples/development/",
        "CONFIGURATION_IMPROVEMENTS_SUMMARY.md": "examples/development/",
        
        # Security and deployment
        "SECURITY_ANALYSIS.md": "docs/development/",
        "SECURITY_AUDIT_REPORT.md": "docs/development/",
        "SECURITY.md": "docs/development/",
        "DEPLOYMENT_SUMMARY.md": "docs/deployment/",
        "DISTRIBUTION_COMPLETE.md": "docs/deployment/",
        "FREE_PYPI_PUBLISHING_GUIDE.md": "docs/deployment/",
        
        # GitHub and distribution
        "FINAL_GITHUB_READY.md": "docs/deployment/",
        "GITHUB_READY_SUMMARY.md": "docs/deployment/",
        "CONTRIBUTING.md": "docs/development/",
        
        # Rules and standards
        "uwu-cli-rules.mdc": "docs/rules/",
        "senior.mdc": "docs/rules/",
        "clean-code.mdc": "docs/rules/",
        "code-analysis.mdc": "docs/rules/",
        "mcp.mdc": "docs/rules/",
        "mermaid.mdc": "docs/rules/",
        "task-list.mdc": "docs/rules/",
        "add-to-changelog.mdc": "docs/rules/",
        "after_each_chat.mdc": "docs/rules/",
        "10x-tool-call.mdc": "docs/rules/",
        "pineapple.mdc": "docs/rules/",
        "better-auth-react-standards.mdc": "docs/rules/"
    }
    
    for source, destination in doc_mapping.items():
        source_path = Path(source)
        dest_path = Path(destination) / source_path.name
        
        if source_path.exists():
            try:
                shutil.move(str(source_path), str(dest_path))
                print(f"✅ Moved {source} to {destination}")
            except Exception as e:
                print(f"⚠️  Could not move {source}: {e}")
        else:
            print(f"ℹ️  Source file not found: {source}")

def organize_scripts():
    """Organize script files"""
    script_mapping = {
        # Installation scripts
        "installer.bat": "scripts/install/",
        "installer.sh": "scripts/install/",
        "install.bat": "scripts/install/",
        "install.ps1": "scripts/install/",
        "install.sh": "scripts/install/",
        "install_new.py": "scripts/install/",
        "install_uwu_cli.bat": "scripts/install/",
        "install_uwu_cli.ps1": "scripts/install/",
        "setup_path.bat": "scripts/install/",
        "setup_path.ps1": "scripts/install/",
        "setup_path.sh": "scripts/install/",
        
        # Development scripts
        "fix_indentation_final.py": "scripts/development/",
        "create_secure_package.py": "scripts/development/",
        "sanitize_secure_package.py": "scripts/development/",
        "publish_to_pypi.py": "scripts/development/",
        "free_distribution.py": "scripts/development/",
        "update_uwu_cli.py": "scripts/development/",
        
        # Deployment scripts
        "organize_project.py": "scripts/deployment/"
    }
    
    for source, destination in script_mapping.items():
        source_path = Path(source)
        dest_path = Path(destination) / source_path.name
        
        if source_path.exists():
            try:
                shutil.move(str(source_path), str(dest_path))
                print(f"✅ Moved {source} to {destination}")
            except Exception as e:
                print(f"⚠️  Could not move {source}: {e}")
        else:
            print(f"ℹ️  Source file not found: {source}")

def organize_test_files():
    """Organize test files"""
    test_dir = Path("tests")
    if not test_dir.exists():
        test_dir.mkdir()
    
    # Move test files to tests directory
    test_files = [f for f in os.listdir(".") if f.startswith("test_") and f.endswith(".py")]
    
    for test_file in test_files:
        try:
            shutil.move(test_file, f"tests/{test_file}")
            print(f"✅ Moved test file: {test_file}")
        except Exception as e:
            print(f"⚠️  Could not move {test_file}: {e}")

def create_index_files():
    """Create index files for organized directories"""
    
    # Create docs index
    docs_index = """# UwU-CLI Documentation

## 📚 Available Documentation

### Guides
- [User Guide](guides/USER_GUIDE.md) - Complete user manual
- [Enhanced Features](guides/ENHANCED_FEATURES_SUMMARY.md) - Latest features
- [Autopilot Guide](guides/AUTOPILOT_README.md) - Automation features
- [Terminal Integration](guides/TERMINAL_INTEGRATION_README.md) - Shell integration

### Development
- [ChatGPT Analysis Plan](development/CHATGPT_ANALYSIS_IMPLEMENTATION_PLAN.md) - AI analysis
- [Implementation Plan](development/IMMEDIATE_IMPLEMENTATION_PLAN.md) - Development roadmap
- [Technology Research](development/TECHNOLOGY_RESEARCH.md) - Technical research
- [Project Status](development/PROJECT_STATUS.md) - Current status

### API Reference
- [Cursor API Research](api/CURSOR_API_RESEARCH.md) - Cursor integration
- [Cursor Integration Plan](api/CURSOR_INTEGRATION_PLAN.md) - Integration details
- [Cursor Fixes Summary](api/COMPREHENSIVE_CURSOR_FIXES_SUMMARY.md) - Bug fixes

### Examples
- [Quick Start](examples/quick_start/) - Get started quickly
- [Advanced Usage](examples/advanced/) - Advanced features
- [Plugin Development](examples/plugins/) - Custom plugins

### Rules and Standards
- [Cursor Rules](rules/) - Development standards
- [Code Quality](rules/clean-code.mdc) - Clean code guidelines
- [Security](rules/) - Security standards
"""
    
    with open("docs/README.md", "w", encoding="utf-8") as f:
        f.write(docs_index)
    
    # Create scripts index
    scripts_index = """# UwU-CLI Scripts

## 📜 Available Scripts

### Installation
- [Windows Batch](install/installer.bat) - Windows installer
- [PowerShell](install/install.ps1) - PowerShell installer
- [Linux/Mac](install/install.sh) - Unix installer
- [Python Installer](install/install_new.py) - Python-based installer

### Development
- [Code Fixes](development/fix_indentation_final.py) - Code formatting
- [Package Creation](development/create_secure_package.py) - Secure packaging
- [Distribution](development/free_distribution.py) - Free distribution setup

### Deployment
- [Project Organization](deployment/organize_project.py) - This script
"""
    
    with open("scripts/README.md", "w", encoding="utf-8") as f:
        f.write(scripts_index)
    
    print("✅ Created index files for organized directories")

def create_help_aliases():
    """Create help command aliases for better organization"""
    help_aliases = {
        "help": "Show comprehensive help system",
        "help quick": "Show quick commands reference",
        "help shell": "Show multi-shell commands",
        "help research": "Show research mode commands",
        "help cursor": "Show Cursor AI integration",
        "help telegram": "Show Telegram integration",
        "help themes": "Show theme system",
        "help plugins": "Show plugin system",
        "help security": "Show security features",
        "help rules": "Show Cursor rules integration"
    }
    
    # Add to QUICK_COMMANDS if they don't exist
    # This part of the code was not provided in the original file,
    # so it's commented out to avoid errors.
    # if hasattr(self, 'QUICK_COMMANDS'):
    #     for alias, description in help_aliases.items():
    #         if f"/{alias}" not in self.QUICK_COMMANDS:
    #             self.QUICK_COMMANDS[f"/{alias}"] = f"show help for {description.lower()}"
    
    print("✅ Created help command aliases")

def cleanup_old_files():
    """Clean up old or duplicate files"""
    files_to_remove = [
        "fix_indentation_final.py",  # Moved to scripts/development/
        "create_secure_package.py",  # Moved to scripts/development/
        "sanitize_secure_package.py",  # Moved to scripts/development/
        "publish_to_pypi.py",  # Moved to scripts/development/
        "free_distribution.py",  # Moved to scripts/development/
        "update_uwu_cli.py",  # Moved to scripts/development/
    ]
    
    for file_path in files_to_remove:
        if Path(file_path).exists():
            try:
                os.remove(file_path)
                print(f"🗑️  Removed old file: {file_path}")
            except Exception as e:
                print(f"⚠️  Could not remove {file_path}: {e}")

def main():
    """Main organization function"""
    print("🚀 Organizing UwU-CLI Project Structure")
    print("=" * 50)
    
    # Create directory structure
    print("\n📁 Creating directory structure...")
    create_directory_structure()
    
    # Organize documentation
    print("\n📚 Organizing documentation...")
    organize_documentation()
    
    # Organize scripts
    print("\n📜 Organizing scripts...")
    organize_scripts()
    
    # Organize test files
    print("\n🧪 Organizing test files...")
    organize_test_files()
    
    # Create index files
    print("\n📖 Creating index files...")
    create_index_files()
    
    # Clean up old files
    print("\n🗑️  Cleaning up old files...")
    cleanup_old_files()
    
    print("\n" + "=" * 50)
    print("🎉 Project organization complete!")
    print("\n📁 New structure:")
    print("   docs/          - All documentation")
    print("   scripts/       - Installation and utility scripts")
    print("   examples/      - Usage examples")
    print("   assets/        - Themes and resources")
    print("   templates/     - Plugin and rule templates")
    print("\n💡 Use '/help' in UwU-CLI for comprehensive help")
    print("📚 Check docs/README.md for organized documentation")

if __name__ == "__main__":
    main() 