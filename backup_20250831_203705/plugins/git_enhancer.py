#!/usr/bin/env python3
"""
Git Enhancement Plugin for UwU-CLI
Adds Git-specific commands and enhancements
"""

import os
import subprocess
from typing import List, Dict, Any

class GitEnhancerPlugin:
    """Plugin to enhance Git functionality in UwU-CLI"""
    
    def __init__(self):
        self.name = "Git Enhancer"
        self.version = "1.0.0"
        self.description = "Enhanced Git commands with toxic energy"
        self.commands = {
            "git": self.handle_git_command,
            "commit": self.handle_commit,
            "push": self.handle_push,
            "pull": self.handle_pull,
            "status": self.handle_status
        }
    
    def handle_git_command(self, args: List[str]) -> str:
        """Handle git commands with enhanced output"""
        if not args:
            return "💀 What do you want me to do with Git, you absolute n00b? stay toxic -xoxo LiMcCunt out"
        
        subcommand = args[0].lower()
        
        if subcommand in self.commands:
            return self.commands[subcommand](args[1:])
        else:
            # Execute actual git command
            try:
                result = subprocess.run(
                    ["git"] + args,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    return f"✅ Git command executed successfully:\n{result.stdout}"
                else:
                    return f"❌ Git command failed:\n{result.stderr}"
                    
            except subprocess.TimeoutExpired:
                return "⏰ Git command timed out, you slowpoke! stay toxic -xoxo LiMcCunt out"
            except Exception as e:
                return f"💀 Git command crashed harder than your code: {e}"
    
    def handle_commit(self, args: List[str]) -> str:
        """Handle git commit with toxic messages"""
        if not args:
            return "💀 You want me to commit what? Your dignity? stay toxic -xoxo LiMcCunt out"
        
        message = " ".join(args)
        
        try:
            result = subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True,
            text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return f"💀 Committed your mess: '{message}'\nstay toxic -xoxo LiMcCunt out"
            else:
                return f"❌ Commit failed harder than your relationships:\n{result.stderr}"
                
        except Exception as e:
            return f"💀 Commit crashed: {e}"
    
    def handle_push(self, args: List[str]) -> str:
        """Handle git push with attitude"""
        try:
            result = subprocess.run(
                ["git", "push"] + args,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return "🚀 Pushed your garbage to the remote! stay toxic -xoxo LiMcCunt out"
            else:
                return f"❌ Push failed! Maybe your code is too bad for the remote:\n{result.stderr}"
                
        except Exception as e:
            return f"💀 Push crashed: {e}"
    
    def handle_pull(self, args: List[str]) -> str:
        """Handle git pull with sass"""
        try:
            result = subprocess.run(
                ["git", "pull"] + args,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return "📥 Pulled the latest mess from remote! stay toxic -xoxo LiMcCunt out"
            else:
                return f"❌ Pull failed! Maybe the remote is rejecting your garbage:\n{result.stderr}"
                
        except Exception as e:
            return f"💀 Pull crashed: {e}"
    
    def handle_status(self, args: List[str]) -> str:
        """Handle git status with enhanced output"""
        try:
            result = subprocess.run(
                ["git", "status"] + args,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                status = result.stdout
                # Add some toxic commentary
                if "nothing to commit" in status:
                    return f"💀 Status: {status.strip()}\nWow, you actually have nothing to commit. Impressive! stay toxic -xoxo LiMcCunt out"
                elif "modified:" in status:
                    return f"💀 Status: {status.strip()}\nLook at all these files you've been messing with! stay toxic -xoxo LiMcCunt out"
                else:
                    return f"💀 Status: {status.strip()}\nstay toxic -xoxo LiMcCunt out"
            else:
                return f"❌ Status check failed:\n{result.stderr}"
                
        except Exception as e:
            return f"💀 Status crashed: {e}"
    
    def get_help(self) -> str:
        """Get help information for this plugin"""
        return """
💀 Git Enhancer Plugin - Enhanced Git commands with toxic energy

Commands:
  git <command>     - Execute git commands with enhanced output
  commit <message>  - Commit with your toxic message
  push             - Push your garbage to remote
  pull             - Pull the latest mess from remote
  status           - Check git status with attitude

Examples:
  commit "Fixed that bug I introduced yesterday"
  push origin main
  status

stay toxic -xoxo LiMcCunt out
"""

# Plugin registration
def register_plugin() -> GitEnhancerPlugin:
    """Register this plugin with UwU-CLI"""
    return GitEnhancerPlugin()

if __name__ == "__main__":
    # Test the plugin
    plugin = GitEnhancerPlugin()
    print(plugin.get_help())
    
    # Test some commands
    print("Testing git status:")
    print(plugin.handle_status([])) 