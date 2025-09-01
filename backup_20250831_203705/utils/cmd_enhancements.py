# utils/cmd_enhancements.py
"""
CMD enhancements for UwU-CLI
Provides better command execution, suggestions, and CMD compatibility
"""

import os
import subprocess
import shlex
from pathlib import Path
from typing import List, Dict, Any, Optional

class CMDEnhancer:
    """Enhances CMD command execution with better output and suggestions"""
    
    def __init__(self):
        self.common_commands = {
            'dir': 'List directory contents',
            'copy': 'Copy files',
            'move': 'Move files',
            'del': 'Delete files',
            'type': 'Display file contents',
            'echo': 'Display text',
            'set': 'Set environment variables',
            'cd': 'Change directory',
            'md': 'Create directory',
            'rd': 'Remove directory',
            'ren': 'Rename files',
            'cls': 'Clear screen',
            'help': 'Show command help',
            'exit': 'Exit command prompt'
        }
        
        # Enhanced command mappings
        self.cmd_aliases = {
            'ls': 'dir',
            'cp': 'copy',
            'mv': 'move',
            'rm': 'del',
            'cat': 'type',
            'mkdir': 'md',
            'rmdir': 'rd',
            'clear': 'cls'
        }
    
    def execute_command(self, cmd: str, cwd: str = None) -> str:
        """Execute a command with CMD enhancements"""
        try:
            # Handle aliases
            cmd_parts = cmd.split()
            if cmd_parts[0] in self.cmd_aliases:
                cmd_parts[0] = self.cmd_aliases[cmd_parts[0]]
                cmd = ' '.join(cmd_parts)
            
            # Special handling for common commands
            if cmd_parts[0].lower() == 'dir':
                return self._enhanced_dir(cwd)
            elif cmd_parts[0].lower() == 'help':
                return self._show_cmd_help()
            elif cmd_parts[0].lower() == 'cls':
                os.system('cls' if os.name == 'nt' else 'clear')
                return ""
            
            # Execute with subprocess
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=cwd,
                timeout=30
            )
            
            output = []
            if result.stdout:
                output.append(result.stdout)
            if result.stderr:
                output.append(f"⚠️  {result.stderr}")
            
            return '\n'.join(output) if output else ""
            
        except subprocess.TimeoutExpired:
            return "❌ Command timed out after 30 seconds"
        except Exception as e:
            return f"❌ Command execution failed: {str(e)}"
    
    def _enhanced_dir(self, cwd: str = None) -> str:
        """Enhanced directory listing with colors and icons"""
        try:
            if not cwd:
                cwd = os.getcwd()
            
            items = os.listdir(cwd)
            dirs = []
            files = []
            
            for item in items:
                item_path = os.path.join(cwd, item)
                if os.path.isdir(item_path):
                    dirs.append(f"📁 {item}")
                else:
                    # Add file type icons
                    ext = os.path.splitext(item)[1].lower()
                    icon = self._get_file_icon(ext)
                    files.append(f"{icon} {item}")
            
            # Sort and format
            dirs.sort()
            files.sort()
            
            output = [f"📂 Directory of {cwd}\n"]
            output.extend(dirs)
            output.extend(files)
            output.append(f"\n📊 {len(dirs)} directories, {len(files)} files")
            
            return '\n'.join(output)
            
        except Exception as e:
            return f"❌ Directory listing failed: {str(e)}"
    
    def _get_file_icon(self, extension: str) -> str:
        """Get appropriate icon for file type"""
        icon_map = {
            '.py': '🐍',
            '.js': '📜',
            '.ts': '📘',
            '.html': '🌐',
            '.css': '🎨',
            '.json': '📋',
            '.xml': '📄',
            '.txt': '📝',
            '.md': '📖',
            '.exe': '⚙️',
            '.dll': '🔧',
            '.bat': '🦇',
            '.ps1': '💻',
            '.zip': '📦',
            '.rar': '📦',
            '.7z': '📦',
            '.jpg': '🖼️',
            '.jpeg': '🖼️',
            '.png': '🖼️',
            '.gif': '🎬',
            '.mp4': '🎥',
            '.mp3': '🎵',
            '.wav': '🎵'
        }
        return icon_map.get(extension, '📄')
    
    def _show_cmd_help(self) -> str:
        """Show enhanced CMD help"""
        help_text = [
            "╔════════════════════════════════════════════╗",
            "║              CMD Commands                   ║",
            "╚════════════════════════════════════════════╝",
            "",
            "📁 File & Directory Commands:",
            "  dir                    - List directory contents",
            "  copy <source> <dest>   - Copy files",
            "  move <source> <dest>   - Move files",
            "  del <file>             - Delete files",
            "  type <file>            - Display file contents",
            "  md <dirname>           - Create directory",
            "  rd <dirname>           - Remove directory",
            "  ren <old> <new>        - Rename files",
            "",
            "🔧 System Commands:",
            "  cd <path>              - Change directory",
            "  cls                    - Clear screen",
            "  echo <text>            - Display text",
            "  set                    - Show environment variables",
            "  help                   - Show this help",
            "  exit                   - Exit command prompt",
            "",
            "💡 Tips:",
            "  - Use tab completion for commands and files",
            "  - Commands are case-insensitive",
            "  - Use quotes for paths with spaces",
            "  - Type 'help <command>' for specific help"
        ]
        return '\n'.join(help_text)
    
    def get_command_suggestions(self, partial: str) -> List[str]:
        """Get command suggestions based on partial input"""
        suggestions = []
        partial_lower = partial.lower()
        
        # Check common commands
        for cmd in self.common_commands.keys():
            if cmd.lower().startswith(partial_lower):
                suggestions.append(cmd)
        
        # Check aliases
        for alias in self.cmd_aliases.keys():
            if alias.lower().startswith(partial_lower):
                suggestions.append(alias)
        
        return suggestions[:10]  # Limit to 10 suggestions
    
    def get_file_suggestions(self, partial: str, cwd: str = None) -> List[str]:
        """Get file/directory suggestions based on partial input"""
        if not cwd:
            cwd = os.getcwd()
        
        suggestions = []
        partial_lower = partial.lower()
        
        try:
            # Get directory and base name
            dir_path = os.path.dirname(partial) if os.path.dirname(partial) else cwd
            base_name = os.path.basename(partial)
            
            if os.path.exists(dir_path):
                for item in os.listdir(dir_path):
                    if item.lower().startswith(base_name.lower()):
                        full_path = os.path.join(dir_path, item)
                        if os.path.isdir(full_path):
                            suggestions.append(full_path + os.sep)
                        else:
                            suggestions.append(full_path)
        except:
            pass
        
        return suggestions[:10]  # Limit to 10 suggestions
    
    def format_command_output(self, output: str, command: str) -> str:
        """Format command output with enhancements"""
        if not output:
            return ""
        
        # Add command header
        formatted = f"🔧 {command}\n"
        formatted += "─" * (len(command) + 4) + "\n"
        formatted += output
        
        return formatted
    
    def get_command_info(self, command: str) -> str:
        """Get information about a specific command"""
        cmd_lower = command.lower()
        
        # Check common commands
        if cmd_lower in self.common_commands:
            return self.common_commands[cmd_lower]
        
        # Check aliases
        if cmd_lower in self.cmd_aliases:
            original = self.cmd_aliases[cmd_lower]
            return f"Alias for '{original}': {self.common_commands.get(original, 'Unknown command')}"
        
        return "Command not found. Type 'help' for available commands."

# Utility functions
def get_command_suggestions(partial: str) -> List[str]:
    """Get command suggestions"""
    enhancer = CMDEnhancer()
    return enhancer.get_command_suggestions(partial)

def get_file_suggestions(partial: str, cwd: str = None) -> List[str]:
    """Get file suggestions"""
    enhancer = CMDEnhancer()
    return enhancer.get_file_suggestions(partial, cwd) 