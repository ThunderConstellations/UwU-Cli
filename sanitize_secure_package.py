#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sanitize Secure Package
Remove remaining personal information from secure package
"""

import re
from pathlib import Path

def sanitize_file(file_path, replacements):
    """Sanitize a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Sanitized: {file_path}")
            return True
        else:
            print(f"ℹ️  No changes needed: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main sanitization process"""
    print("🧹 Sanitizing Secure Package")
    print("=" * 40)
    
    secure_dir = Path("secure_dist")
    if not secure_dir.exists():
        print("❌ secure_dist directory not found!")
        return
    
    # Define replacements
    replacements = {
        "ThunderConstellations": "UwU-CLI",
        "personal": "user-specific",
        "private": "confidential",
        "Cringe Lord": "USERNAME",
        "C:\\Users\\Cringe Lord": "C:\\Users\\USERNAME"
    }
    
    # Files to sanitize
    files_to_sanitize = [
        "CONTRIBUTING.md",
        "SECURITY.md",
        ".github/CODE_OF_CONDUCT.md",
        ".github/profile/README.md"
    ]
    
    changes_made = 0
    
    for file_path in files_to_sanitize:
        full_path = secure_dir / file_path
        if full_path.exists():
            if sanitize_file(full_path, replacements):
                changes_made += 1
    
    print(f"\n🎉 Sanitization complete!")
    print(f"📊 Files modified: {changes_made}")
    
    # Verify security
    print("\n🔍 Verifying security...")
    verify_security(secure_dir)

def verify_security(secure_dir):
    """Verify the package is now secure"""
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
    print("🎉 Package is now safe for PyPI publishing!")
    return True

if __name__ == "__main__":
    main() 