#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced UwU-CLI Help System
Provides comprehensive, organized, and dynamic help by introspecting the CLI state.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class HelpSystem:
    def __init__(self, uwu_cli):
        self.uwu_cli = uwu_cli
        self.help_data = self._load_help_data()
        self.cursor_rules = self._load_cursor_rules()
    
    def _load_help_data(self) -> Dict[str, Any]:
        """Load static help data structure"""
        return {
            "quick_commands": {
                "title": "Quick Commands",
                "description": "Short, efficient commands for common tasks",
                "categories": {
                    "core": {
                        "title": "Core Commands",
                        "commands": {
                            "/c": "Continue improving",
                            "/e": "Explain code + create .md",
                            "/p": "Research + plan + .md",
                            "/cc": "Continue from previous"
                        }
                    },
                    "streamlined": {
                        "title": "Streamlined Commands",
                        "commands": {
                            "/f": "Fix bugs",
                            "/o": "Optimize code",
                            "/t": "Add tests",
                            "/r": "Refactor code",
                            "/d": "Debug help",
                            "/h": "Get help",
                            "/s": "Save file",
                            "/g": "Git add"
                        }
                    }
                }
            },
            "multi_shell": {
                "title": "Multi-Shell Commands",
                "description": "Execute commands in specific shells",
                "prefixes": {
                    "cmd:": "Windows CMD",
                    "ps1:": "PowerShell",
                    "bash:": "Bash (WSL)",
                    "cs:": "Cursor AI"
                }
            },
            "research_modes": {
                "title": "Research Mode Commands",
                "description": "Specialized AI assistance modes",
                "modes": {
                    "deep:": "Deep research",
                    "review:": "Code review",
                    "audit:": "Project audit"
                }
            }
        }
    
    def _load_cursor_rules(self) -> Dict[str, str]:
        """Load available Cursor rules from filesystem"""
        rules_dir = Path(".cursor/rules")
        rules = {}
        if rules_dir.exists():
            for rule_file in rules_dir.glob("*.mdc"):
                rules[rule_file.name] = "Cursor development rule"
        return rules

    def get_dynamic_info(self) -> str:
        """Introspect UwUCLI for registered plugins and aliases"""
        info = "\n🔌 **Registered Plugins:**\n"
        if hasattr(self.uwu_cli, 'plugins') and self.uwu_cli.plugins:
            for plugin in self.uwu_cli.plugins:
                # If plugin is a module or dict
                if isinstance(plugin, dict):
                    name = plugin.get('name', 'Unknown Plugin')
                else:
                    name = getattr(plugin, 'name', str(plugin))
                info += f"  • {name}\n"
        else:
            info += "  • No plugins loaded\n"

        info += "\n🔗 **User Aliases:**\n"
        if hasattr(self.uwu_cli, 'config'):
            aliases = self.uwu_cli.config.get('aliases', {})
            if aliases:
                for alias, cmd in aliases.items():
                    info += f"  • {alias} -> {cmd}\n"
            else:
                info += "  • No aliases defined\n"
        return info

    def get_main_help(self) -> str:
        """Get main help overview with dynamic info"""
        help_text = "🚀 **UwU-CLI Help System**\n"
        help_text += "=" * 40 + "\n"
        
        for category, data in self.help_data.items():
            help_text += f"• **{data['title']}** - {data['description']}\n"
        
        help_text += self.get_dynamic_info()
        help_text += "\n💡 Use `/help <category>` for details | `/topics` to list all"
        
        return help_text

    def get_category_help(self, category: str) -> str:
        """Get detailed help for a category"""
        if category not in self.help_data:
            return f"❌ Category '{category}' not found."

        data = self.help_data[category]
        help_text = f"📚 **{data['title']}**\n"
        help_text += f"{data['description']}\n\n"
        
        if category == "quick_commands":
            for cat_name, cat_data in data["categories"].items():
                help_text += f"🔹 {cat_data['title']}\n"
                for cmd, desc in cat_data["commands"].items():
                    help_text += f"  {cmd} - {desc}\n"
        elif category == "multi_shell":
            for prefix, desc in data["prefixes"].items():
                help_text += f"  {prefix} - {desc}\n"
        elif category == "research_modes":
            for mode, desc in data["modes"].items():
                help_text += f"  {mode} - {desc}\n"

        return help_text

    def get_help(self, topic: str = None) -> str:
        """Main entry point for help requests"""
        if not topic or topic == "main":
            return self.get_main_help()
        
        topic = topic.lower().strip()
        if topic in self.help_data:
            return self.get_category_help(topic)

        return self.get_main_help()

def get_command_suggestions(partial: str) -> List[str]:
    """Compatibility function for command suggestions"""
    from utils.cmd_enhancements import CMDEnhancer
    return CMDEnhancer().get_command_suggestions(partial)
