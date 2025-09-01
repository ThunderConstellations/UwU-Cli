"""
Update Utility for UwU-CLI
Provides easy update mechanism for existing installations
"""

import os
import sys
import json
import shutil
import subprocess
import requests
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

class UwUUpdater:
    """Handles UwU-CLI updates safely"""
    
    def __init__(self):
        self.current_version = "2.0.0"
        self.github_repo = "https://github.com/UwU-CLI/UwU-Cli"
        self.update_dir = Path.home() / ".uwu-cli" / "updates"
        self.backup_dir = Path.home() / ".uwu-cli" / "backups"
        
        # Ensure directories exist
        self.update_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def check_for_updates(self) -> Tuple[bool, str, str]:
        """Check if updates are available"""
        try:
            # Get latest release info from GitHub
            api_url = "https://api.github.com/repos/UwU-CLI/UwU-Cli/releases/latest"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                release_info = response.json()
                latest_version = release_info["tag_name"].lstrip("v")
                
                if self._version_compare(latest_version, self.current_version) > 0:
                    return True, latest_version, release_info.get("body", "")
                else:
                    return False, latest_version, "Already up to date"
            else:
                return False, self.current_version, f"Failed to check updates: {response.status_code}"
                
        except Exception as e:
            return False, self.current_version, f"Error checking updates: {str(e)}"
    
    def _version_compare(self, version1: str, version2: str) -> int:
        """Compare version strings"""
        v1_parts = [int(x) for x in version1.split('.')]
        v2_parts = [int(x) for x in version2.split('.')]
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_part = v1_parts[i] if i < len(v1_parts) else 0
            v2_part = v2_parts[i] if i < len(v2_parts) else 0
            
            if v1_part > v2_part:
                return 1
            elif v1_part < v2_part:
                return -1
        
        return 0
    
    def download_update(self, version: str) -> bool:
        """Download the latest update"""
        try:
            # Download source code
            source_url = f"{self.github_repo}/archive/refs/tags/v{version}.zip"
            zip_path = self.update_dir / f"uwu-cli-{version}.zip"
            
            print(f"📥 Downloading UwU-CLI v{version}...")
            response = requests.get(source_url, stream=True, timeout=30)
            
            if response.status_code == 200:
                with open(zip_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Extract the update
                import zipfile
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(self.update_dir)
                
                return True
            else:
                print(f"❌ Failed to download update: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error downloading update: {str(e)}")
            return False
    
    def backup_current_installation(self) -> bool:
        """Create backup of current installation"""
        try:
            current_dir = Path.cwd()
            backup_path = self.backup_dir / f"backup-{self.current_version}-{int(os.time())}"
            
            print(f"💾 Creating backup at: {backup_path}")
            shutil.copytree(current_dir, backup_path, ignore=shutil.ignore_patterns(
                '__pycache__', '*.pyc', '.git', 'node_modules', '.venv', 'venv'
            ))
            
            return True
        except Exception as e:
            print(f"❌ Failed to create backup: {str(e)}")
            return False
    
    def apply_update(self, version: str) -> bool:
        """Apply the downloaded update"""
        try:
            extracted_dir = self.update_dir / f"UwU-Cli-{version}"
            if not extracted_dir.exists():
                print(f"❌ Update files not found: {extracted_dir}")
                return False
            
            current_dir = Path.cwd()
            
            # Copy new files, preserving user configs
            for item in extracted_dir.iterdir():
                if item.name in ['.git', '.gitignore', 'README.md', 'LICENSE']:
                    continue
                
                target = current_dir / item.name
                if item.is_dir():
                    if target.exists():
                        shutil.rmtree(target)
                    shutil.copytree(item, target)
                else:
                    shutil.copy2(item, target)
            
            print(f"✅ Update v{version} applied successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to apply update: {str(e)}")
            return False
    
    def rollback_update(self) -> bool:
        """Rollback to previous version if update fails"""
        try:
            # Find most recent backup
            backups = sorted(self.backup_dir.glob("backup-*"), key=lambda x: x.stat().st_mtime, reverse=True)
            
            if not backups:
                print("❌ No backups found for rollback")
                return False
            
            latest_backup = backups[0]
            current_dir = Path.cwd()
            
            print(f"🔄 Rolling back to: {latest_backup}")
            
            # Remove current files (except user configs)
            for item in current_dir.iterdir():
                if item.name in ['.git', '.gitignore', 'config', '.uwu-cli']:
                    continue
                
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            
            # Restore from backup
            for item in latest_backup.iterdir():
                if item.name in ['.git', '.gitignore']:
                    continue
                
                target = current_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, target)
                else:
                    shutil.copy2(item, target)
            
            print("✅ Rollback completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Rollback failed: {str(e)}")
            return False
    
    def update(self, force: bool = False) -> bool:
        """Perform complete update process"""
        print("🚀 UwU-CLI Update Utility")
        print(f"Current version: {self.current_version}")
        
        # Check for updates
        has_update, latest_version, message = self.check_for_updates()
        
        if not has_update and not force:
            print(f"✅ {message}")
            return True
        
        if has_update:
            print(f"🆕 New version available: {latest_version}")
            print(f"📝 Release notes:\n{message}")
        
        # Confirm update
        if not force:
            response = input("Do you want to proceed with the update? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("❌ Update cancelled")
                return False
        
        try:
            # Create backup
            if not self.backup_current_installation():
                print("❌ Backup failed, cannot proceed with update")
                return False
            
            # Download update
            if not self.download_update(latest_version):
                print("❌ Download failed")
                return False
            
            # Apply update
            if not self.apply_update(latest_version):
                print("❌ Update failed, attempting rollback...")
                if self.rollback_update():
                    print("✅ Rollback successful")
                else:
                    print("❌ Rollback failed - manual intervention required")
                return False
            
            print("🎉 Update completed successfully!")
            print("💡 Restart UwU-CLI to use the new version")
            return True
            
        except Exception as e:
            print(f"❌ Update process failed: {str(e)}")
            print("🔄 Attempting rollback...")
            if self.rollback_update():
                print("✅ Rollback successful")
            else:
                print("❌ Rollback failed - manual intervention required")
            return False
    
    def show_update_info(self):
        """Show update information and status"""
        print("🚀 UwU-CLI Update Information")
        print(f"Current version: {self.current_version}")
        
        has_update, latest_version, message = self.check_for_updates()
        
        if has_update:
            print(f"🆕 New version available: {latest_version}")
            print(f"📝 Release notes:\n{message}")
            print("\n💡 Run 'update' command to install the update")
        else:
            print(f"✅ {message}")
        
        # Show backup information
        backups = list(self.backup_dir.glob("backup-*"))
        if backups:
            print(f"\n💾 Available backups: {len(backups)}")
            for backup in sorted(backups, key=lambda x: x.stat().st_mtime, reverse=True)[:3]:
                backup_name = backup.name
                backup_time = os.path.getctime(backup)
                print(f"   {backup_name} - {os.ctime(backup_time)}")

# Global instance
_updater = None

def get_updater() -> UwUUpdater:
    """Get the global updater instance"""
    global _updater
    if _updater is None:
        _updater = UwUUpdater()
    return _updater 