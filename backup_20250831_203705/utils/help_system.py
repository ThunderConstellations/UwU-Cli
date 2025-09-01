#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UwU-CLI Help System
Provides comprehensive, organized help for all features
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
        """Load help data from structured sources"""
        return {
            "quick_commands": {
                "title": "Quick Commands",
                "description": "Short, efficient commands for common tasks",
                "categories": {
                    "core": {
                        "title": "Core Commands",
                        "description": "Essential commands for basic functionality",
                        "commands": {
                            "/c": "Continue improving and ensure quick commands work",
                            "/e": "Explain code and show example usage",
                            "/p": "Research and plan issues and improvements",
                            "/cc": "Continue from where previous session left off"
                        }
                    },
                    "streamlined": {
                        "title": "Streamlined Commands",
                        "description": "New, efficient commands for daily use",
                        "commands": {
                            "/cs": "Continue as planned",
                            "/f": "Fix any issues found",
                            "/o": "Optimize code for performance",
                            "/t": "Test functionality thoroughly",
                            "/r": "Review code for improvements",
                            "/d": "Debug issues step by step",
                            "/h": "Help understanding",
                            "/s": "Show current status",
                            "/g": "Generate solutions"
                        }
                    },
                    "infinite": {
                        "title": "Infinite Mode Commands",
                        "description": "Continuous AI assistance until completion",
                        "commands": {
                            "/infinite": "Continue working until completion",
                            "/infiniteon": "Start infinite mode",
                            "/infiniteoff": "Stop infinite mode"
                        }
                    }
                }
            },
            "multi_shell": {
                "title": "Multi-Shell Commands",
                "description": "Execute commands in specific shells",
                "prefixes": {
                    "cmd:": "Execute in Windows CMD",
                    "ps1:": "Execute in PowerShell",
                    "bash:": "Execute in Bash (WSL on Windows)",
                    "cs:": "Send to Cursor AI"
                },
                "examples": [
                    "cmd: echo Hello from CMD",
                    "ps1: Write-Host 'Hello from PowerShell'",
                    "bash: echo 'Hello from Bash'",
                    "cs: continue working on this project"
                ]
            },
            "research_modes": {
                "title": "Research Mode Commands",
                "description": "Specialized AI assistance modes",
                "modes": {
                    "deep:": "Comprehensive research mode with multiple sources",
                    "review:": "Code review mode for systematic analysis",
                    "audit:": "Full project audit mode for security and quality"
                },
                "examples": [
                    "deep: improve this codebase",
                    "review: analyze this code",
                    "audit: check for security issues"
                ]
            },
            "cursor_integration": {
                "title": "Cursor AI Integration",
                "description": "Seamless AI assistance in your terminal",
                "features": [
                    "AI-powered code completion",
                    "Context-aware assistance",
                    "Real-time AI responses",
                    "Integration with Cursor IDE"
                ],
                "setup": "Ensure Cursor IDE is installed and configured"
            },
            "telegram_integration": {
                "title": "Telegram Remote Control",
                "description": "Control UwU-CLI remotely via Telegram bot",
                "features": [
                    "Remote command execution",
                    "Real-time AI assistance",
                    "Multi-shell support",
                    "Infinite mode control"
                ],
                "setup": "Configure .autopilot.json with your Telegram bot token"
            },
            "themes": {
                "title": "Theme System",
                "description": "Customizable appearance and prompts",
                "available_themes": [
                    "default - Clean, professional appearance",
                    "uwu - Enhanced UwU experience",
                    "cringe - UwU-style with colors",
                    "matrix - Green terminal aesthetic",
                    "rainbow - Colorful and vibrant"
                ],
                "customization": "Modify themes in config/main.json"
            },
            "plugins": {
                "title": "Plugin System",
                "description": "Extensible architecture for community contributions",
                "features": [
                    "Hook-based plugin system",
                    "Community plugin marketplace",
                    "Hot reloading capability",
                    "Plugin lifecycle management"
                ],
                "development": "See .cursor/rules/ for plugin development guidelines"
            },
            "security": {
                "title": "Security Features",
                "description": "Production-ready security measures",
                "features": [
                    "Command whitelisting",
                    "PTY-based execution (no shell=True)",
                    "Input validation and sanitization",
                    "Timeout protection",
                    "Secret redaction in logs"
                ]
            },
            "cursor_rules": {
                "title": "Cursor Rules Integration",
                "description": "Development standards and guidelines",
                "rules": {
                    "uwu-cli-rules.mdc": "Master rules for UwU-CLI development",
                    "senior.mdc": "Senior developer standards and best practices",
                    "clean-code.mdc": "Clean code guidelines and principles",
                    "code-analysis.mdc": "Code analysis and quality tools",
                    "mcp.mdc": "MCP server usage guidelines",
                    "mermaid.mdc": "Diagram generation for documentation",
                    "task-list.mdc": "Task management and tracking",
                    "add-to-changelog.mdc": "Changelog management",
                    "after_each_chat.mdc": "Chat session management",
                    "10x-tool-call.mdc": "Automated task progression",
                    "pineapple.mdc": "Special development modes",
                    "better-auth-react-standards.mdc": "Authentication standards"
                }
            }
        }
    
    def _load_cursor_rules(self) -> Dict[str, str]:
        """Load available Cursor rules"""
        rules_dir = Path(".cursor/rules")
        rules = {}
        
        if rules_dir.exists():
            for rule_file in rules_dir.glob("*.mdc"):
                try:
                    with open(rule_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract description if available
                        description = "Cursor development rule"
                        if "description:" in content:
                            desc_line = [line for line in content.split('\n') if line.startswith('description:')]
                            if desc_line:
                                description = desc_line[0].replace('description:', '').strip()
                        rules[rule_file.stem] = description
                except Exception as e:
                    rules[rule_file.stem] = f"Error loading rule: {e}"
        
        return rules
    
    def get_main_help(self) -> str:
        """Get main help overview"""
        help_text = "🚀 UwU-CLI Help System\n"
        help_text += "=" * 50 + "\n\n"
        
        help_text += "📚 Available Help Categories:\n\n"
        
        for category, data in self.help_data.items():
            help_text += f"• {data['title']} - {data['description']}\n"
        
        help_text += "\n💡 Use '/help <category>' for detailed information\n"
        help_text += "🔍 Use '/help search <term>' to search for specific topics\n"
        help_text += "📖 Use '/help rules' to see available Cursor rules\n"
        
        return help_text
    
    def get_category_help(self, category: str) -> str:
        """Get help for a specific category"""
        if category not in self.help_data:
            return f"❌ Category '{category}' not found. Use '/help' to see available categories."
        
        data = self.help_data[category]
        help_text = f"📚 {data['title']}\n"
        help_text += "=" * 50 + "\n\n"
        help_text += f"{data['description']}\n\n"
        
        if category == "quick_commands":
            for cat_name, cat_data in data["categories"].items():
                help_text += f"🔹 {cat_data['title']}\n"
                help_text += f"   {cat_data['description']}\n"
                for cmd, desc in cat_data["commands"].items():
                    help_text += f"   {cmd} - {desc}\n"
                help_text += "\n"
        
        elif category == "multi_shell":
            help_text += "🔹 Available Shells:\n"
            for prefix, desc in data["prefixes"].items():
                help_text += f"   {prefix} {desc}\n"
            help_text += "\n🔹 Examples:\n"
            for example in data["examples"]:
                help_text += f"   {example}\n"
        
        elif category == "research_modes":
            help_text += "🔹 Available Modes:\n"
            for mode, desc in data["modes"].items():
                help_text += f"   {mode} {desc}\n"
            help_text += "\n🔹 Examples:\n"
            for example in data["examples"]:
                help_text += f"   {example}\n"
        
        elif category == "cursor_rules":
            help_text += "🔹 Available Rules:\n"
            for rule, desc in self.cursor_rules.items():
                help_text += f"   {rule} - {desc}\n"
        
        else:
            if "features" in data:
                help_text += "🔹 Features:\n"
                for feature in data["features"]:
                    help_text += f"   • {feature}\n"
            
            if "examples" in data:
                help_text += "\n🔹 Examples:\n"
                for example in data["examples"]:
                    help_text += f"   {example}\n"
            
            if "setup" in data:
                help_text += f"\n🔧 Setup: {data['setup']}\n"
        
        return help_text
    
    def search_help(self, search_term: str) -> str:
        """Search help content for specific terms"""
        search_term = search_term.lower()
        results = []
        
        for category, data in self.help_data.items():
            # Search in category title and description
            if search_term in data['title'].lower() or search_term in data['description'].lower():
                results.append(f"📚 {data['title']} - {data['description']}")
            
            # Search in quick commands
            if category == "quick_commands":
                for cat_name, cat_data in data["categories"].items():
                    for cmd, desc in cat_data["commands"].items():
                        if search_term in cmd.lower() or search_term in desc.lower():
                            results.append(f"⚡ {cmd} - {desc}")
            
            # Search in multi-shell prefixes
            elif category == "multi_shell":
                for prefix, desc in data["prefixes"].items():
                    if search_term in prefix.lower() or search_term in desc.lower():
                        results.append(f"🔌 {prefix} - {desc}")
            
            # Search in research modes
            elif category == "research_modes":
                for mode, desc in data["modes"].items():
                    if search_term in mode.lower() or search_term in desc.lower():
                        results.append(f"🔍 {mode} - {desc}")
        
        if not results:
            return f"🔍 No results found for '{search_term}'. Try different search terms or use '/help' to see all categories."
        
        help_text = f"🔍 Search Results for '{search_term}':\n"
        help_text += "=" * 50 + "\n\n"
        
        for result in results[:10]:  # Limit to 10 results
            help_text += f"{result}\n"
        
        if len(results) > 10:
            help_text += f"\n... and {len(results) - 10} more results. Refine your search for better results."
        
        return help_text
    
    def get_cursor_rules_help(self) -> str:
        """Get help for Cursor rules"""
        help_text = "📖 Cursor Rules Integration\n"
        help_text += "=" * 50 + "\n\n"
        help_text += "This project uses Cursor IDE with comprehensive rules for consistent development.\n\n"
        
        help_text += "🔹 Available Rules:\n"
        for rule, description in self.cursor_rules.items():
            help_text += f"   • {rule} - {description}\n"
        
        help_text += "\n💡 These rules ensure:\n"
        help_text += "   • Consistent code quality\n"
        help_text += "   • Best practices adherence\n"
        help_text += "   • Professional development standards\n"
        help_text += "   • Automated task progression\n"
        
        help_text += "\n📚 Rule files are located in .cursor/rules/\n"
        help_text += "🔧 Rules are automatically applied when using Cursor IDE\n"
        
        return help_text
    
    def get_quick_reference(self) -> str:
        """Get a quick reference card"""
        help_text = "⚡ Quick Reference Card\n"
        help_text += "=" * 50 + "\n\n"
        
        help_text += "🔹 Essential Commands:\n"
        help_text += "   /c, /e, /p, /cc - Core functionality\n"
        help_text += "   /cs, /f, /o, /t - Daily tasks\n"
        help_text += "   /infiniteon, /infiniteoff - AI assistance\n"
        help_text += "   /help - This help system\n\n"
        
        help_text += "🔹 Multi-Shell:\n"
        help_text += "   cmd:, ps1:, bash:, cs: - Shell routing\n\n"
        
        help_text += "🔹 Research Modes:\n"
        help_text += "   deep:, review:, audit: - AI assistance\n\n"
        
        help_text += "🔹 Examples:\n"
        help_text += "   cmd: echo Hello\n"
        help_text += "   cs: continue working\n"
        help_text += "   deep: improve code\n"
        
        return help_text
    
    def get_help(self, topic: str = None) -> str:
        """Main help method"""
        if not topic:
            return self.get_main_help()
        
        topic = topic.lower().strip()
        
        if topic == "rules":
            return self.get_cursor_rules_help()
        elif topic == "quick":
            return self.get_quick_reference()
        elif topic.startswith("search "):
            search_term = topic[7:].strip()
            return self.search_help(search_term)
        elif topic in self.help_data:
            return self.get_category_help(topic)
        else:
            # Try to find partial matches
            for category in self.help_data.keys():
                if topic in category.lower():
                    return self.get_category_help(category)
            
            return f"❌ Topic '{topic}' not found. Use '/help' to see available categories." 