#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Secure PyPI Publishing Script for UwU-CLI
Includes comprehensive security checks before publishing
"""

import os
import subprocess
import sys
import re
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def security_scan():
    """Perform comprehensive security scan before publishing"""
    print("🔒 Performing security scan...")
    
    # Check for personal information patterns
    personal_patterns = [
        r'Cringe Lord',
        r'C:\\Users\\Cringe Lord',
        r'ThunderConstellations',
        r'personal',
        r'private',
        r'@[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # Email addresses
        r'[0-9]{3}-[0-9]{3}-[0-9]{4}',  # Phone numbers
        r'[0-9]{5}(?:-[0-9]{4})?',  # ZIP codes
    ]
    
    # Check for sensitive configuration
    sensitive_files = [
        '.autopilot.json',
        '.telegram_config.json',
        '.env',
        'config/secrets.json',
        'config/auth.json'
    ]
    
    # Check for API keys and tokens
    api_patterns = [
        r'api_key["\']?\s*:\s*["\'][^"\']+["\']',
        r'token["\']?\s*:\s*["\'][^"\']+["\']',
        r'password["\']?\s*:\s*["\'][^"\']+["\']',
        r'secret["\']?\s*:\s*["\'][^"\']+["\']',
    ]
    
    issues_found = []
    
    # Scan all Python and configuration files
    for file_path in Path('.').rglob('*'):
        if file_path.is_file() and file_path.suffix in ['.py', '.json', '.md', '.txt']:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Check for personal information
                    for pattern in personal_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            issues_found.append(f"Personal info found in {file_path}: {pattern}")
                    
                    # Check for API keys
                    for pattern in api_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            issues_found.append(f"Potential API key found in {file_path}: {pattern}")
                            
            except Exception as e:
                print(f"⚠️  Could not read {file_path}: {e}")
    
    # Check for sensitive files
    for sensitive_file in sensitive_files:
        if Path(sensitive_file).exists():
            issues_found.append(f"Sensitive file found: {sensitive_file}")
    
    if issues_found:
        print("❌ Security issues found:")
        for issue in issues_found:
            print(f"   - {issue}")
        print("\n🚨 Publishing blocked due to security issues!")
        return False
    
    print("✅ Security scan passed - no vulnerabilities detected")
    return True

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check if build is installed
    try:
        import build
        print("✅ build package is available")
    except ImportError:
        print("❌ build package not found. Installing...")
        run_command("pip install build", "Installing build package")
    
    # Check if twine is installed
    try:
        import twine
        print("✅ twine package is available")
    except ImportError:
        print("❌ twine package not found. Installing...")
        run_command("pip install twine", "Installing twine package")

def build_package():
    """Build the package distribution"""
    print("🏗️  Building package distribution...")
    
    # Clean previous builds
    run_command("python -m build --clean", "Cleaning previous builds")
    
    # Build source and wheel distributions
    result = run_command("python -m build", "Building package distributions")
    
    if result:
        print("✅ Package built successfully")
        return True
    return False

def check_distribution():
    """Check the built distribution"""
    print("🔍 Checking built distribution...")
    
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ dist directory not found")
        return False
    
    files = list(dist_dir.glob("*"))
    print(f"📦 Found {len(files)} distribution files:")
    for file in files:
        print(f"   - {file.name}")
    
    return len(files) > 0

def publish_to_test_pypi():
    """Publish to Test PyPI first"""
    print("🚀 Publishing to Test PyPI...")
    
    result = run_command("python -m twine upload --repository testpypi dist/*", "Publishing to Test PyPI")
    
    if result:
        print("✅ Published to Test PyPI successfully")
        print("🔗 Test PyPI URL: https://test.pypi.org/project/uwu-cli/")
        return True
    return False

def publish_to_pypi():
    """Publish to PyPI"""
    print("🚀 Publishing to PyPI...")
    
    result = run_command("python -m twine upload dist/*", "Publishing to PyPI")
    
    if result:
        print("✅ Published to PyPI successfully")
        print("🔗 PyPI URL: https://pypi.org/project/uwu-cli/")
        return True
    return False

def main():
    """Main publishing process with security checks"""
    print("🎉 UwU-CLI Secure PyPI Publishing Process")
    print("=" * 60)
    
    # Security scan first
    if not security_scan():
        print("\n🚨 Security scan failed. Publishing blocked.")
        print("Please fix all security issues before attempting to publish.")
        sys.exit(1)
    
    # Check prerequisites
    check_prerequisites()
    
    # Build package
    if not build_package():
        print("❌ Package build failed. Exiting.")
        sys.exit(1)
    
    # Check distribution
    if not check_distribution():
        print("❌ Distribution check failed. Exiting.")
        sys.exit(1)
    
    # Ask user preference
    print("\n📋 Publishing Options:")
    print("1. Publish to Test PyPI only (recommended for testing)")
    print("2. Publish to Test PyPI, then to PyPI")
    print("3. Publish directly to PyPI (not recommended for first time)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        publish_to_test_pypi()
    elif choice == "2":
        if publish_to_test_pypi():
            print("\n⏳ Waiting 5 minutes before publishing to PyPI...")
            import time
            time.sleep(300)
            publish_to_pypi()
    elif choice == "3":
        publish_to_pypi()
    else:
        print("❌ Invalid choice. Exiting.")
        sys.exit(1)
    
    print("\n🎉 Publishing process completed!")
    print("\n📚 Next steps:")
    print("1. Test installation: pip install --index-url https://test.pypi.org/simple/ uwu-cli")
    print("2. Verify functionality: uwu --help")
    print("3. If everything works, publish to main PyPI")

if __name__ == "__main__":
    main() 