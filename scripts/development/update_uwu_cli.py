#!/usr/bin/env python3
"""
UwU-CLI Update Script
Simple update mechanism for existing installations
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_git_available():
    """Check if git is available"""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def update_from_git():
    """Update UwU-CLI from git repository"""
    print("🔄 Updating UwU-CLI from Git repository...")
    
    try:
        # Check if we're in a git repository
        if not Path(".git").exists():
            print("❌ Not in a git repository. Please clone the repository first.")
            return False
        
        # Fetch latest changes
        print("📥 Fetching latest changes...")
        subprocess.run(["git", "fetch", "origin"], check=True)
        
        # Check current branch
        result = subprocess.run(["git", "branch", "--show-current"], 
                              capture_output=True, text=True, check=True)
        current_branch = result.stdout.strip()
        
        # Pull latest changes
        print(f"📥 Pulling latest changes from {current_branch}...")
        subprocess.run(["git", "pull", "origin", current_branch], check=True)
        
        print("✅ Update completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git update failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Update failed: {e}")
        return False

def update_from_zip():
    """Update UwU-CLI from zip file"""
    print("🔄 Updating UwU-CLI from zip file...")
    
    # Look for update zip files
    update_files = list(Path(".").glob("uwu-cli-*.zip"))
    
    if not update_files:
        print("❌ No update zip files found in current directory")
        print("💡 Download the latest release from GitHub and place it here")
        return False
    
    # Use the most recent zip file
    latest_update = max(update_files, key=lambda x: x.stat().st_mtime)
    print(f"📦 Found update file: {latest_update}")
    
    try:
        import zipfile
        
        # Create backup
        backup_dir = Path("backup_before_update")
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        backup_dir.mkdir()
        
        # Backup important files
        important_files = ["uwu_cli.py", "utils/", "config/", "phrases/", "plugins/"]
        for item in important_files:
            if Path(item).exists():
                if Path(item).is_file():
                    shutil.copy2(item, backup_dir / item)
                else:
                    shutil.copytree(item, backup_dir / item, dirs_exist_ok=True)
        
        print(f"💾 Backup created in: {backup_dir}")
        
        # Extract update
        with zipfile.ZipFile(latest_update, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        print("✅ Update extracted successfully!")
        print("💡 Restart UwU-CLI to use the new version")
        return True
        
    except Exception as e:
        print(f"❌ Zip update failed: {e}")
        print("💡 You can restore from backup if needed")
        return False

def check_for_updates():
    """Check if updates are available"""
    print("🔍 Checking for updates...")
    
    if check_git_available():
        try:
            # Check if we're in a git repository
            if Path(".git").exists():
                # Fetch latest info
                subprocess.run(["git", "fetch", "origin"], capture_output=True)
                
                # Check if we're behind
                result = subprocess.run(["git", "rev-list", "--count", "HEAD..origin/main"], 
                                      capture_output=True, text=True, check=True)
                behind_count = int(result.stdout.strip())
                
                if behind_count > 0:
                    print(f"🆕 {behind_count} commits behind origin/main")
                    return True
                else:
                    print("✅ Already up to date!")
                    return False
            else:
                print("ℹ️  Not in a git repository")
                return False
                
        except Exception as e:
            print(f"⚠️  Could not check for updates: {e}")
            return False
    else:
        print("ℹ️  Git not available, cannot check for updates")
        return False

def main():
    """Main update function"""
    print("🚀 UwU-CLI Update Tool")
    print("=" * 40)
    
    # Check for updates
    has_updates = check_for_updates()
    
    if has_updates:
        print("\n🔄 Updates available!")
        response = input("Do you want to update now? (y/N): ").strip().lower()
        
        if response in ['y', 'yes']:
            if check_git_available() and Path(".git").exists():
                success = update_from_git()
            else:
                print("💡 Git not available, trying zip update...")
                success = update_from_zip()
            
            if success:
                print("\n🎉 Update completed successfully!")
                print("💡 Restart UwU-CLI to use the new version")
            else:
                print("\n💥 Update failed. Check the errors above.")
        else:
            print("❌ Update cancelled")
    else:
        print("\n✅ No updates needed")
    
    print("\n💡 Manual update options:")
    print("   1. Use git: git pull origin main")
    print("   2. Download latest release from GitHub")
    print("   3. Run this script again later")

if __name__ == "__main__":
    main() 