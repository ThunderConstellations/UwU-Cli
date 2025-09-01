#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UwU-CLI: The Ultimate Chaotic CMD Replacement
A fully-featured, AI-powered, context-aware CMD replacement that combines 
the functionality of CMD with Clink autosuggestions, chaotic UwU energy, 
automatic clapbacks, and AI assistance.
"""

from utils.cmd_enhancements import CMDEnhancer, get_command_suggestions
from utils.tts import speak, export_text
from utils.config import load_config, save_config, get_alias, set_alias
from utils.ascii_ui import Spinner, print_with_effect, get_colored_prompt
from utils.ai import submit_ai_job, get_job_result, load_config as ai_load_config
from utils.tokenizer import inject_context, context_entities
from utils.autopilot import get_autopilot, send_notification
from utils.telegram_controller import start_telegram_control, stop_telegram_control
from utils.cursor_controller import get_cursor_controller, open_file_in_cursor, open_folder_in_cursor, open_current_in_cursor, send_command_to_cursor, send_shortcut_to_cursor
import os
import sys
import json
import threading
import queue
import subprocess
import time
import random
import shlex
import readline
import glob
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our modules

# ------------------------------
# UwU-CLI Core
# ------------------------------


class UwUCLI:
    def __init__(self):
        self.plugins = []
        self.config = load_config()
        self.ai_config = ai_load_config()

        # Aggregate all phrase roasts
        self.roasts = self._load_all_phrases()

        # Plugin system
        self._load_plugins()

        # AI job queue
        self.ai_jobs = {}
        self.job_counter = 0

        # History file
        self.history_file = Path.home() / ".uwu_history"
        self.history_file.parent.mkdir(exist_ok=True)

        # Current working directory tracking
        self.cwd = os.getcwd()

        # Theme support with colors
        self.current_theme = self.config.get("prompt_style", "toxic")

        # CMD enhancements
        self.cmd_enhancer = CMDEnhancer()

        # Auto-clapback mode (always on)
        self.auto_clapback = True

        # Command suggestions
        self.suggestions = []

        # Command result tracking
        self.last_command_result = None

        # Initialize state manager
        try:
            from utils.state_manager import get_state_manager
            self.state_manager = get_state_manager()
            print("📊 State management system initialized")
        except Exception as e:
            print(f"⚠️  State management failed to initialize: {e}")
            self.state_manager = None

        # Setup readline for autosuggestions
        self._setup_readline()

        print("UwU-CLI CMD replacement activated! Stay wavy~ nyah x3")

        # Send autopilot startup notification
        try:
            autopilot = get_autopilot()
            if autopilot and autopilot.enabled:
                autopilot.notify_cli_start()
        except Exception as e:
            print(f"⚠️  Autopilot notification failed: {e}")

        # Start Telegram command control (optional)
        try:
            # Check if Telegram is enabled in config
            telegram_enabled = self.config.get("telegram_enabled", True)
            if telegram_enabled:
                if start_telegram_control(self._execute_telegram_command):
                    print("🎮 Telegram command control activated")
                    # Send cursor chat integration notification
                    self._send_cursor_chat_notification(
                        "🚀 UwU-CLI started in Cursor terminal! All output will be captured and sent to Telegram.")
                else:
                    print("⚠️  Telegram command control failed to start")
            else:
                print("📱 Telegram disabled in configuration")
        except Exception as e:
            print(f"⚠️  Telegram command control error: {e}")
            print("💡 To disable Telegram, set 'telegram_enabled': false in your config")

    def _setup_readline(self):
        """Setup readline for autosuggestions and history"""
        try:
            # Import readline conditionally (not available on Windows)
            try:
                import readline
            except ImportError:
                # Windows doesn't have readline, use alternative
                try:
                    import pyreadline3 as readline
                except ImportError:
                    print("⚠️  Readline not available - tab completion disabled")
                    return

            # Load history
            if self.history_file.exists():
                readline.read_history_file(str(self.history_file))

            # Set history length
            readline.set_history_length(1000)

            # Setup tab completion
            readline.set_completer(self._completer)
            readline.parse_and_bind('tab: complete')

        except Exception as e:
            print(f"⚠️  Readline setup failed: {e}")

    def _execute_telegram_command(self, command: str) -> str:
        """Execute command received from Telegram"""
        try:
            # Handle Cursor commands specially
            if command.lower().startswith("cursor:cmd "):
                cursor_command = command[11:].strip()
                # Remove quotes if present
                if (cursor_command.startswith("'") and cursor_command.endswith("'")) or (cursor_command.startswith('"') and cursor_command.endswith('"')):
                    cursor_command = cursor_command[1:-1]
                result = send_command_to_cursor(cursor_command)
                return result

            elif command.lower().startswith("cursor:shortcut "):
                shortcut = command[16:].strip()
                # Remove quotes if present
                if (shortcut.startswith("'") and shortcut.endswith("'")) or (shortcut.startswith('"') and shortcut.endswith('"')):
                    shortcut = shortcut[1:-1]
                result = send_shortcut_to_cursor(shortcut)
                return result

            elif command.lower() == "cursor:help":
                return "📝 Cursor Editor Commands:\n" + \
                       "  cursor:cmd <command>   - Send command to Cursor\n" + \
                       "  cursor:shortcut <key>  - Send keyboard shortcut to Cursor\n" + \
                       "  cursor:help            - Show this help\n\n" + \
                       "💡 Examples:\n" + \
                       "  • cursor:cmd 'git: add'\n" + \
                       "  • cursor:cmd 'python: run'\n" + \
                       "  • cursor:shortcut 'ctrl+s'"

            elif command.lower() == "cursor:status":
                controller = get_cursor_controller()
                result = controller.get_status()
                return result

            elif command.lower() == "cursor:open .":
                result = open_current_in_cursor()
                return result

            elif command.lower().startswith("cursor:open "):
                file_path = command[12:].strip()
                result = open_file_in_cursor(file_path)
                return result

            elif command.lower().startswith("cursor:folder "):
                folder_path = command[14:].strip()
                result = open_folder_in_cursor(folder_path)
                return result

            elif command.lower() == "cursor:new":
                controller = get_cursor_controller()
                result = controller.new_window()
                return result

            elif command.lower() == "cursor:close":
                controller = get_cursor_controller()
                result = controller.close_all()
                return result

            # Handle other built-in commands
            elif command.lower() in ["help", "pwd", "ls", "dir", "clear", "cls"]:
                if command.lower() == "help":
                    return self._get_help_text()
                elif command.lower() in ["pwd", "pwd"]:
                    return f"📁 Current directory: {self.cwd}"
                elif command.lower() in ["ls", "ls"]:
                    return self._get_directory_listing()
                elif command.lower() in ["clear", "cls"]:
                    # Note: Can't clear screen in Telegram, just return message
                    return "Screen cleared (use clear/cls in CLI for actual clearing)"

            # Execute other commands using the shell
            result = self.shell_command(command)
            return result if result else "Command executed successfully"

        except Exception as e:
            return f"Error executing command: {str(e)}"

    def _get_help_text(self) -> str:
        """Get help text for Telegram responses"""
        return """╔════════════════════════════════════════════╗
║              UwU-CLI Help                   ║
╚════════════════════════════════════════════╝

🎮 Core Commands:
  uwu                    - Toggle UwU mode
  ai:rewrite <text>      - AI-powered text rewriting
  ai:roast <text>        - AI-powered roasts
  theme <name>           - Change prompt theme
  config show            - Show configuration
  help                   - Show this help
  exit                   - Exit UwU-CLI

🔧 Utility Commands:
  pwd                    - Show current directory
  ls/dir                 - List directory contents
  clear/cls              - Clear screen
  history                - Show command history

🚀 Enhanced Quick Commands:
  /e                     - Explain code + create .md file
  /p                     - Research + plan + .md file
  /cc                    - Continue where left off
  /c                     - Standard continue command
  /f                     - Fix bugs
  /o                     - Optimize code
  /t                     - Add tests
  /r                     - Refactor code
  /d                     - Debug help
  /h                     - Get help
  /s                     - Save file
  /g                     - Git add

🔄 Infinite Mode Commands:
  /infiniteon            - Enable infinite AI assistance
  /infiniteoff           - Disable infinite mode
  /infinite              - Show infinite mode status

🤖 AI Chat Commands:
  cursor:cmd <command>   - Send to Cursor AI
  cs: <command>          - Quick Cursor AI (same as above)
  chat:new <title>       - Start new AI conversation
  chat:list              - List all AI conversations
  chat:open <id>         - Open specific conversation
  chat:search <query>    - Search conversations
  chat:export <id>       - Export conversation
  chat:stats             - Show conversation statistics

🔬 Advanced Research Modes:
  deep: <topic>          - Deep research mode
  review: <target>       - Code review mode
  audit: <scope>         - Full project audit mode

💻 Multi-Shell Support:
  cmd: <command>         - Execute in CMD shell
  ps1: <command>         - Execute in PowerShell
  bash: <command>        - Execute in Bash (if available)

📝 Cursor Commands:
  cursor:help            - Show Cursor help
  cursor:status          - Check Cursor availability
  cursor:suggestions     - Show AI chat suggestions

🎮 Telegram Commands:
  telegram:start         - Start remote control
  telegram:stop          - Stop remote control
  telegram:status        - Check remote control status
  telegram:enable        - Enable Telegram control
  telegram:disable       - Disable Telegram control

💡 Tips:
  - Use tab completion for commands and files
  - Commands are case-insensitive
  - Use quotes for paths with spaces
  - /infiniteon for continuous AI assistance
  - Use deep:, review:, audit: for comprehensive analysis"""

    def _get_directory_listing(self) -> str:
        """Get directory listing for Telegram responses"""
        try:
            items = os.listdir(self.cwd)
            dirs = []
            files = []

            for item in items:
                item_path = os.path.join(self.cwd, item)
                if os.path.isdir(item_path):
                    dirs.append(f"📁 {item}")
                else:
                    files.append(f"📄 {item}")

            result = f"📂 Directory of {self.cwd}\n\n"
            if dirs:
                result += "📁 Directories:\n" + "\n".join(sorted(dirs)) + "\n\n"
            if files:
                result += "📄 Files:\n" + "\n".join(sorted(files))

            return result
        except Exception as e:
            return f"❌ Error listing directory: {str(e)}"

    def _send_cursor_chat_notification(self, message: str):
        """Send notification to Telegram about Cursor chat activity"""
        try:
            from utils.telegram_controller import get_telegram_controller

            controller = get_telegram_controller()
            if controller:
                controller.send_notification(f"📝 Cursor Chat: {message}")
        except Exception as e:
            print(f"⚠️  Failed to send Cursor chat notification: {e}")

    def _capture_cursor_output(self, output: str):
        """Capture Cursor output and send to Telegram"""
        if output and len(output.strip()) > 0:
            # Send to Telegram as cursor chat
            self._send_cursor_chat_notification(
                f"Cursor Output:\n{output[:500]}{'...' if len(output) > 500 else ''}")

    def _completer(self, text, state):
        """Tab completion for commands and files"""
        if state == 0:
            # Get suggestions based on current input
            self.suggestions = self._get_completions(text)

        if state < len(self.suggestions):
            return self.suggestions[state]
        return None

    def _get_completions(self, text):
        """Get command and file completions"""
        completions = []

        # Command completions using enhanced suggestions
        if not text or text.startswith(' '):
            # Show common commands
            common_cmds = ['uwu', 'ai:rewrite', 'ai:roast',
                           'theme', 'config', 'help', 'exit']
            completions.extend(
                [cmd for cmd in common_cmds if cmd.startswith(text.lstrip())])

            # Add enhanced command suggestions
            try:
                from utils.cmd_enhancements import get_command_suggestions
                enhanced_suggestions = get_command_suggestions(text.lstrip())
                completions.extend(enhanced_suggestions)
            except ImportError:
                pass

        # File completions using enhanced suggestions
        if text and not text.startswith(' '):
            try:
                from utils.cmd_enhancements import get_file_suggestions
                file_suggestions = get_file_suggestions(text, os.getcwd())
                completions.extend(file_suggestions)
            except ImportError:
                # Fallback to basic file completion
                try:
                    dir_path = os.path.dirname(
                        text) if os.path.dirname(text) else '.'
                    base_name = os.path.basename(text)

                    if os.path.exists(dir_path):
                        for item in os.listdir(dir_path):
                            if item.startswith(base_name):
                                full_path = os.path.join(dir_path, item)
                                if os.path.isdir(full_path):
                                    completions.append(full_path + os.sep)
                                else:
                                    completions.append(full_path)
                except:
                    pass

        return completions

    def _load_all_phrases(self):
        """Load all phrase modules"""
        phrases = []

        # Pokémon phrases
        try:
            from phrases.pokemon import pokemon_roasts
            phrases.extend(pokemon_roasts)
        except ImportError:
            pass

        # Digimon phrases
        try:
            from phrases.digimon import digimon_roasts
            phrases.extend(digimon_roasts)
        except ImportError:
            pass

        # MTG phrases
        try:
            from phrases.mtg import mtg_roasts
            phrases.extend(mtg_roasts)
        except ImportError:
            pass

        # Yu-Gi-Oh! phrases
        try:
            from phrases.yugioh import yugioh_roasts
            phrases.extend(yugioh_roasts)
        except ImportError:
            pass

        # Cringey phrases
        try:
            from phrases.cringey import cringey_roasts
            phrases.extend(cringey_roasts)
        except ImportError:
            pass

        # Fallback phrases if none loaded
        if not phrases:
            phrases = [
                {"character": "Default",
                    "roast": "UwU~ Your input is giving chaotic energy!"},
                {"character": "Default", "roast": "Rawr x3 - Stay sparkly, senpai~"},
                {"character": "Default",
                    "roast": "OwO notices ur message... it's a vibe!"}
            ]

        return phrases

    def _load_plugins(self):
        """Load all plugins from plugins directory"""
        plugins_dir = Path(__file__).parent / "plugins"
        if plugins_dir.exists():
            for plugin_file in plugins_dir.glob("*.py"):
                if plugin_file.name != "__init__.py":
                    try:
                        # Import plugin
                        spec = __import__(
                            f"plugins.{plugin_file.stem}", fromlist=["register"])
                        if hasattr(spec, "register"):
                            plugin_hooks = spec.register(self)
                            self.plugins.append(plugin_hooks)
                            print(f"🔌 Loaded plugin: {plugin_file.stem}")
                    except Exception as e:
                        print(
                            f"⚠️  Failed to load plugin {plugin_file.stem}: {e}")

        # Run plugin on_start hooks
        for plugin in self.plugins:
            if "on_start" in plugin and callable(plugin["on_start"]):
                try:
                    plugin["on_start"]()
                except Exception as e:
                    print(f"⚠️  Plugin on_start error: {e}")

    def register_plugin(self, hooks):
        """Register plugin hooks"""
        self.plugins.append(hooks)
        if "on_start" in hooks and callable(hooks["on_start"]):
            hooks["on_start"]()

    def run_plugins_on_input(self, user_input):
        """Run all plugin on_input hooks"""
        for plugin in self.plugins:
            if "on_input" in plugin and callable(plugin["on_input"]):
                try:
                    result = plugin["on_input"](user_input)
                    if result is not None:
                        user_input = result
                except Exception as e:
                    print(f"⚠️  Plugin on_input error: {e}")
        return user_input

    def run_plugins_on_command(self, command, args):
        """Run all plugin on_command hooks"""
        for plugin in self.plugins:
            if "on_command" in plugin and callable(plugin["on_command"]):
                try:
                    handled = plugin["on_command"](command, args)
                    if handled:
                        return True
                except Exception as e:
                    print(f"⚠️  Plugin on_command error: {e}")
        return False

    def run_plugins_on_shutdown(self):
        """Run all plugin on_shutdown hooks"""
        for plugin in self.plugins:
            if "on_shutdown" in plugin and callable(plugin["on_shutdown"]):
                try:
                    plugin["on_shutdown"]()
                except Exception as e:
                    print(f"⚠️  Plugin on_shutdown error: {e}")

    def get_automatic_clapback(self, user_input: str) -> str:
        """Get an automatic clapback based on user input context"""
        # Always return a clapback - no need to ask!
        roast = random.choice(self.roasts)["roast"]

        # Inject context from user input
        roast = inject_context(roast, user_input)

        # Add some variety to the delivery
        delivery_styles = [
            f"💥 {roast}",
            f"⚡ {roast}",
            f"🔥 {roast}",
            f"✨ {roast}",
            f"💫 {roast}"
        ]

        return random.choice(delivery_styles)

    def handle_ai_command(self, user_input):
        """Handle AI commands and return job ID"""
        if user_input.lower().startswith("ai:rewrite "):
            prompt = user_input.replace("ai:rewrite ", "")
            job_id = submit_ai_job(
                f"Rewrite this text in a fun, engaging way: {prompt}", "openrouter")
        elif user_input.lower().startswith("ai:roast "):
            prompt = user_input.replace("ai:roast ", "")
            job_id = submit_ai_job(
                f"Create a playful, sassy roast about: {prompt}", "openrouter")
        elif user_input.lower().startswith("ai:script "):
            prompt = user_input.replace("ai:script ", "")
            job_id = submit_ai_job(
                f"Create a Python script that: {prompt}. Include comments and error handling.", "openrouter")
        elif user_input.lower().startswith("ai:cmd "):
            prompt = user_input.replace("ai:cmd ", "")
            job_id = submit_ai_job(
                f"Convert this to a Windows CMD command: {prompt}", "openrouter")
        elif user_input.lower().startswith("ai:explain "):
            prompt = user_input.replace("ai:explain ", "")
            job_id = submit_ai_job(
                f"Explain this in simple terms: {prompt}", "openrouter")
        elif user_input.lower().startswith("ai:debug "):
            prompt = user_input.replace("ai:debug ", "")
            job_id = submit_ai_job(
                f"Help debug this issue: {prompt}. Provide step-by-step solutions.", "openrouter")
        elif user_input.lower().startswith("ai:optimize "):
            prompt = user_input.replace("ai:optimize ", "")
            job_id = submit_ai_job(
                f"Optimize this code/process: {prompt}. Focus on performance and best practices.", "openrouter")
        else:
            # Generic AI assistance
            job_id = submit_ai_job(user_input, "openrouter")

        self.ai_jobs[job_id] = user_input
        return job_id

    def shell_command(self, cmd):
        """Execute shell command with CMD enhancements"""
        try:
            # Handle case-insensitive commands
            cmd_lower = cmd.lower().strip()

            # Update working directory
            if cmd_lower.startswith("cd "):
                new_dir = cmd[3:].strip()
                if new_dir == "~":
                    new_dir = str(Path.home())
                os.chdir(new_dir)
                self.cwd = os.getcwd()
                print(f"📁 Changed directory to: {self.cwd}")
                return f"📁 Changed directory to: {self.cwd}"

            # Handle common case-insensitive commands
            elif cmd_lower in ["pwd", "pwd", "pwd"]:
                result = f"📁 Current directory: {self.cwd}"
                print(result)
                return result

            elif cmd_lower in ["ls", "ls", "ls"]:
                # Use dir command for Windows compatibility
                result = self.cmd_enhancer.execute_command("dir", cwd=self.cwd)
                if result:
                    print(result)
                    return result
                return "Command executed successfully (no output)"

            elif cmd_lower in ["clear", "cls", "cls"]:
                os.system('cls' if os.name == 'nt' else 'clear')
                return "Screen cleared"

            else:
                # Execute other commands with CMD enhancements
                result = self.cmd_enhancer.execute_command(cmd, cwd=self.cwd)
                if result:
                    print(result)
                    return result
                return "Command executed successfully (no output)"

        except Exception as e:
            error_msg = f"❌ Shell command error: {e}"
            print(error_msg)
            return error_msg

    def handle_aliases(self, user_input):
        """Handle command aliases"""
        parts = user_input.split()
        if not parts:
            return user_input

        alias_cmd = parts[0].lower()  # Make case-insensitive

        # Built-in aliases for common commands
        builtin_aliases = {
            "pwd": "pwd",
            "ls": "dir",
            "clear": "cls",
            "help": "help",
            "exit": "exit",
            "quit": "exit",
            "bye": "exit"
        }

        # Check built-in aliases first
        if alias_cmd in builtin_aliases:
            parts[0] = builtin_aliases[alias_cmd]
            return " ".join(parts)

        # Check user-defined aliases
        resolved = get_alias(alias_cmd)
        if resolved:
            return resolved + " " + " ".join(parts[1:])

        return user_input

    def builtin_commands(self, parts):
        """Handle built-in UwU-CLI commands"""
        cmd = parts[0].lower()  # Make case-insensitive
        args = parts[1:]

        if cmd == "pwd":
            print(f"📁 Current directory: {self.cwd}")
            return True
        elif cmd == "history":
            if self.history_file.exists():
                with open(self.history_file, "r") as f:
                    history = f.read().strip()
                    if history:
                        print("📚 Command History:")
                        print(history)
                    else:
                        print("📚 No command history yet")
            else:
                print("📚 No command history file found")
            return True
        elif cmd == "export":
            text = " ".join(args)
            if text:
                export_text(text)
                print(f"💾 Exported: {text}")
            return True
        elif cmd == "tts":
            text = " ".join(args)
            if text:
                speak(text)
                print(f"🔊 TTS: {text}")
            return True
        elif cmd == "theme":
            if args:
                theme = args[0].lower()
                if theme in ["uwu", "feral", "wizard", "emo", "rainbow", "neon", "pastel"]:
                    self.current_theme = theme
                    self.config["prompt_style"] = theme
                    save_config(self.config)
                    print(f"🎨 Theme changed to: {theme}")
                else:
                    print(
                        f"❌ Unknown theme: {theme}. Available: uwu, feral, wizard, emo, rainbow, neon, pastel")
            else:
                print(f"🎨 Current theme: {self.current_theme}")
            return True
        elif cmd == "help":
            self.print_help()
            return True
        elif cmd == "config":
            if args:
                if args[0] == "show":
                    print("⚙️  Current configuration:")
                    print(json.dumps(self.config, indent=2))
                elif args[0] == "set" and len(args) >= 3:
                    key = args[1]
                    value = " ".join(args[2:])
                    self.config[key] = value
                    save_config(self.config)
                    print(f"⚙️  Set {key} = {value}")
                else:
                    print("Usage: config show | config set <key> <value>")
            else:
                print("Usage: config show | config set <key> <value>")
            return True
        elif cmd == "alias":
            if args:
                if args[0] == "list":
                    aliases = self.config.get("aliases", {})
                    if aliases:
                        print("🔗 Current aliases:")
                        for alias, command in aliases.items():
                            print(f"  {alias} -> {command}")
                    else:
                        print("🔗 No aliases defined")
                elif args[0] == "set" and len(args) >= 3:
                    alias_name = args[1]
                    command = " ".join(args[2:])
                    set_alias(alias_name, command)
                    print(f"🔗 Set alias: {alias_name} -> {command}")
                elif args[0] == "remove" and len(args) >= 2:
                    alias_name = args[1]
                    aliases = self.config.get("aliases", {})
                    if alias_name in aliases:
                        del aliases[alias_name]
                        self.config["aliases"] = aliases
                        save_config(self.config)
                        print(f"🔗 Removed alias: {alias_name}")
                    else:
                        print(f"❌ Alias not found: {alias_name}")
                else:
                    print(
                        "Usage: alias list | alias set <name> <command> | alias remove <name>")
            else:
                print(
                    "Usage: alias list | alias set <name> <command> | alias remove <name>")
            return True
        elif cmd == "chat":
            return self._handle_chat_commands(args)
        elif cmd == "telegram":
            return self._handle_telegram_commands(args)

        return False

    def print_help(self):
        """Print help information"""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║                    UwU-CLI Help                              ║
╚══════════════════════════════════════════════════════════════╝

🎮 AI Commands:
  ai:rewrite <text>     - AI-assisted rewriting
  ai:roast <target>     - AI-assisted roasting
  ai:script <task>      - AI-generated Python scripts
  ai:cmd <description>  - AI-generated CMD commands
  ai:status <job_id>    - Check AI job progress

🔧 Built-in Commands:
  pwd                   - Show current directory
  history               - Show command history
  theme [name]          - Change theme (uwu/feral/wizard/emo/rainbow/neon/pastel)
  config show           - Show configuration
  config set <key> <val> - Set configuration
  alias list            - List aliases
  alias set <name> <cmd> - Set alias
  alias remove <name>   - Remove alias
  help                  - Show this help

🐚 CMD Commands:
  All standard CMD commands work normally:
  dir, copy, move, del, type, etc.

🎨 Themes:
  uwu     - Soft UwU style
  feral   - Chaotic energy
  wizard  - Arcane magic
  emo     - Depressive aesthetic
  rainbow - Colorful rainbow
  neon    - Bright neon
  pastel  - Soft pastels

🔌 Plugins:
  Plugins are automatically loaded from the plugins/ directory
  Each plugin can add custom commands and behaviors

📝 Cursor Editor Commands:
  cursor:open <file>     - Open file in Cursor
  cursor:open .          - Open current folder in Cursor
  cursor:folder <path>   - Open folder in Cursor
  cursor:new             - Open new Cursor window
  cursor:close           - Close all Cursor windows
  cursor:status          - Check Cursor availability
  cursor:cmd <command>   - Send command to Cursor
  cursor:shortcut <key>  - Send keyboard shortcut to Cursor
  cursor:help            - Show Cursor help

🎮 Telegram Remote Control:
  telegram:start         - Start remote command control
  telegram:stop          - Stop remote command control
  telegram:status        - Check remote control status

💡 Features:
  - Automatic clapbacks on every command
  - Tab completion for commands and files
  - Command history with readline
  - Context-aware AI responses
  - Colorful themed prompts
  - Full CMD compatibility
  - Remote control via Telegram
  - Cursor editor integration
        """
        print(help_text)

    def get_prompt(self):
        """Get the current colorful themed prompt"""
        cwd = os.path.basename(self.cwd) if self.cwd != str(
            Path.home()) else "~"
        return get_colored_prompt(self.current_theme, cwd)

    def start(self):
        """Start the UwU-CLI REPL"""
        try:
            while True:
                try:
                    prompt = self.get_prompt()
                    user_input = input(prompt).strip()

                    # Skip empty input
                    if not user_input:
                        continue

                    # Save to history
                    with open(self.history_file, "a") as f:
                        f.write(f"{user_input}\n")

                    # Run plugin input hooks
                    user_input = self.run_plugins_on_input(user_input)

                    # Handle aliases
                    user_input = self.handle_aliases(user_input)

                    # Split into parts
                    parts = user_input.split()
                    if not parts:
                        continue

                    # Check for exit
                    if user_input.lower() in ["exit", "quit", "bye"]:
                        break

                    # Check built-in commands first
                    if self.builtin_commands(parts):
                        continue

                    # Plugin command handling
                    if self.run_plugins_on_command(parts[0], parts[1:]):
                        continue

                    # AI-assisted commands
                    if user_input.lower().startswith(("ai:rewrite ", "ai:roast ", "ai:script ", "ai:cmd ", "ai:explain ", "ai:debug ", "ai:optimize ")):
                        job_id = self.handle_ai_command(user_input)
                        print(f"🤖 AI job submitted! Job ID: {job_id}")
                        print("💡 Use 'ai:status <job_id>' to check progress")
                        continue

                    # AI status check
                    if user_input.lower().startswith("ai:status "):
                        try:
                            job_id = int(user_input.split()[1])
                            result = get_job_result(job_id)
                            if result:
                                print(f"🤖 AI Result: {result}")
                            else:
                                print(f"⏳ Job {job_id} is still processing...")
                        except (ValueError, IndexError):
                            print("❌ Usage: ai:status <job_id>")
                        continue

                    # Autopilot test command
                    if user_input.lower() == "autopilot:test":
                        try:
                            success = send_notification(
                                "🧪 Test message from UwU-CLI!", "Autopilot Test")
                            if success:
                                print("✅ Autopilot test notification sent!")
                            else:
                                print("❌ Autopilot test failed")
                        except Exception as e:
                            print(f"❌ Autopilot test error: {e}")
                        continue

                    # Autopilot status command
                    if user_input.lower() == "autopilot:status":
                        try:
                            autopilot = get_autopilot()
                            if autopilot and autopilot.enabled:
                                print(
                                    f"✅ Autopilot enabled with adapters: {autopilot.adapters}")
                            else:
                                print("❌ Autopilot is disabled")
                        except Exception as e:
                            print(f"❌ Autopilot status error: {e}")
                        continue

                    # Telegram control commands
                    if user_input.lower() == "telegram:start":
                        try:
                            if start_telegram_control(self._execute_telegram_command):
                                print("✅ Telegram command control started!")
                            else:
                                print("❌ Failed to start Telegram control")
                        except Exception as e:
                            print(f"❌ Telegram control error: {e}")
                        continue

                    if user_input.lower() == "telegram:stop":
                        try:
                            stop_telegram_control()
                            print("✅ Telegram command control stopped!")
                        except Exception as e:
                            print(f"❌ Telegram control error: {e}")
                        continue

                    if user_input.lower() == "telegram:status":
                        try:
                            from utils.telegram_controller import get_telegram_controller
                            controller = get_telegram_controller()
                            if controller and controller.running:
                                print("✅ Telegram command control is running")
                            else:
                                print("❌ Telegram command control is stopped")
                        except Exception as e:
                            print(f"❌ Telegram status error: {e}")
                        continue

                    if user_input.lower().startswith("cursor:folder "):
                        try:
                            # Remove "cursor:folder "
                            folder_path = user_input[14:].strip()
                            result = open_folder_in_cursor(folder_path)
                            print(result)
                        except Exception as e:
                            print(f"❌ Cursor folder error: {e}")
                        continue

                    if user_input.lower() == "cursor:new":
                        try:
                            controller = get_cursor_controller()
                            result = controller.new_window()
                            print(result)
                        except Exception as e:
                            print(f"❌ Cursor new window error: {e}")
                        continue

                    if user_input.lower() == "cursor:close":
                        try:
                            controller = get_cursor_controller()
                            result = controller.close_all()
                            print(result)
                        except Exception as e:
                            print(f"❌ Cursor close error: {e}")
                        continue

                    if user_input.lower() == "cursor:status":
                        try:
                            controller = get_cursor_controller()
                            result = controller.get_status()
                            print(result)
                        except Exception as e:
                            print(f"❌ Cursor status error: {e}")
                        continue

                    # Quick commands (fast access) - enhanced with special features
                    if user_input.startswith('/') and len(user_input) <= 3:
                        try:
                            from utils.cursor_controller import get_quick_commands, expand_quick_command
                            quick_commands = get_quick_commands()
                            
                            if user_input in quick_commands:
                                expanded_command = expand_quick_command(
                                    user_input)
                                print(
                                    f"🚀 Quick command '{user_input}' → '{expanded_command}'")

                                # Enhanced quick commands with special handling
                                if user_input.lower() == "/e":
                                    # /e = explain and create .md file
                                    enhanced_command = "explain this code in detail and create a comprehensive markdown file documenting everything"
                                    print(
                                        f"📝 Enhanced command: {enhanced_command}")
                                    result = send_command_to_cursor(
                                        enhanced_command)
                                elif user_input.lower() == "/p":
                                    # /p = research and plan with .md file
                                    enhanced_command = "heavily research and plan for issues being faced as well as improvements to the code. Create a comprehensive .md file for everything we need to get done and reference it from now on till complete"
                                    print(
                                        f"📋 Enhanced command: {enhanced_command}")
                                    result = send_command_to_cursor(
                                        enhanced_command)
                                elif user_input.lower() == "/cc":
                                    # /cc = continue where we left off
                                    enhanced_command = "continue with where we left off, reference the previous conversation and plan"
                                    print(
                                        f"🔄 Enhanced command: {enhanced_command}")
                                    result = send_command_to_cursor(
                                        enhanced_command)
                                else:
                                    # Standard quick command
                                    result = send_command_to_cursor(
                                        expanded_command)

                                print(result)

                                # Store in conversation manager
                                try:
                                    from utils.ai_conversation_manager import get_conversation_manager
                                    manager = get_conversation_manager()
                                    title = f"Quick Command - {user_input} - {enhanced_command[:30]}{'...' if len(enhanced_command) > 30 else ''}"
                                    conv_id = manager.start_conversation(
                                        title, tags=['quick-command', 'cursor-ai'])
                                    manager.add_message(
                                        conv_id, 'user', enhanced_command)
                                    print(
                                        f"💾 Stored in conversation: {conv_id}")
                                except Exception as e:
                                    print(
                                        f"⚠️  Failed to store conversation: {e}")
                            else:
                                print(f"❌ Unknown quick command: {user_input}")
                                print("💡 Available quick commands:")
                                for cmd, desc in quick_commands.items():
                                    print(f"   {cmd} → {desc}")
                            continue
                        except Exception as e:
                            print(f"❌ Quick command error: {e}")
                            continue
                    
                    # Infinite Mode Commands
                    if user_input.lower() == "/infiniteon":
                        try:
                            from utils.cursor_controller import enable_infinite_mode
                            result = enable_infinite_mode(
                                "Continuous AI assistance mode", "Work on tasks until completion")
                            print(result)
                        except Exception as e:
                            print(f"❌ Failed to enable infinite mode: {e}")
                        continue

                    if user_input.lower() == "/infiniteoff":
                        try:
                            from utils.cursor_controller import disable_infinite_mode
                            result = disable_infinite_mode()
                            print(result)
                        except Exception as e:
                            print(f"❌ Failed to disable infinite mode: {e}")
                        continue

                    if user_input.lower() == "/infinite":
                        try:
                            from utils.cursor_controller import get_infinite_status
                            result = get_infinite_status()
                            print(result)
                        except Exception as e:
                            print(f"❌ Failed to get infinite status: {e}")
                        continue

                    # Cursor AI chat commands - these go to Cursor AI, not terminal
                    if user_input.lower().startswith("cursor:cmd "):
                        try:
                            # Remove "cursor:cmd "
                            command = user_input[11:].strip()
                            # Remove quotes if present
                            if (command.startswith("'") and command.endswith("'")) or (command.startswith('"') and command.endswith('"')):
                                command = command[1:-1]

                            # This is an AI chat command - send to Cursor AI
                            print(f"🤖 Sending to Cursor AI: '{command}'")
                            result = send_command_to_cursor(command)
                            print(result)

                            # Store in conversation manager
                            try:
                                from utils.ai_conversation_manager import get_conversation_manager
                                manager = get_conversation_manager()
                                title = f"AI Chat - {command[:30]}{'...' if len(command) > 30 else ''}"
                                conv_id = manager.start_conversation(
                                    title, tags=['cursor-ai'])
                                manager.add_message(conv_id, 'user', command)
                                print(f"💾 Stored in conversation: {conv_id}")
                            except Exception as e:
                                print(f"⚠️  Failed to store conversation: {e}")

                        except Exception as e:
                            print(f"❌ Cursor AI command error: {e}")
                        continue

                    if user_input.lower().startswith("cursor:shortcut "):
                        try:
                            # Remove "cursor:shortcut "
                            shortcut = user_input[16:].strip()
                            # Remove quotes if present
                            if (shortcut.startswith("'") and shortcut.endswith("'")) or (shortcut.startswith('"') and shortcut.endswith('"')):
                                shortcut = shortcut[1:-1]
                            result = send_shortcut_to_cursor(shortcut)
                            print(result)
                        except Exception as e:
                            print(f"❌ Cursor shortcut error: {e}")
                        continue

                    if user_input.lower() == "cursor:help":
                        try:
                            from utils.cursor_controller import get_cursor_help
                            help_text = get_cursor_help()
                            print(help_text)
                        except Exception as e:
                            print(f"❌ Cursor help error: {e}")
                        continue
                    
                    if user_input.lower() == "cursor:suggestions":
                        try:
                            from utils.cursor_controller import get_ai_suggestions
                            suggestions = get_ai_suggestions()
                            print("💡 **AI Chat Suggestions**")
                            print("Use these commands to interact with Cursor's AI:")
                            for i, suggestion in enumerate(suggestions, 1):
                                print(f"  {i:2d}. {suggestion}")
                            print(
                                f"\n💡 Total: {len(suggestions)} suggestions available")
                            print(
                                "🎯 Use: cursor:cmd '<suggestion>' or quick command /c, /e, /f, etc.")
                        except Exception as e:
                            print(f"❌ Cursor suggestions error: {e}")
                        continue

                    # Handle other cursor commands (case-insensitive)
                    if user_input.lower().startswith("cursor:"):
                        # Extract the subcommand
                        # Remove "cursor:" prefix
                        subcommand = user_input[7:].lower()

                        if subcommand.startswith("open "):
                            # Remove "open " prefix
                            file_path = subcommand[5:].strip()
                            if file_path == ".":
                                result = open_current_in_cursor()
                            else:
                                result = open_file_in_cursor(file_path)
                            print(result)
                        elif subcommand.startswith("folder "):
                            # Remove "folder " prefix
                            folder_path = subcommand[7:].strip()
                            result = open_folder_in_cursor(folder_path)
                            print(result)
                        elif subcommand == "new":
                            controller = get_cursor_controller()
                            result = controller.new_window()
                            print(result)
                        elif subcommand == "close":
                            controller = get_cursor_controller()
                            result = controller.close_all()
                            print(result)
                        elif subcommand == "status":
                            controller = get_cursor_controller()
                            result = controller.get_status()
                            print(result)
                        else:
                            print(f"❌ Unknown cursor subcommand: {subcommand}")
                            print(
                                "💡 Available: open, folder, new, close, status, help, suggestions")
                        continue

                    # Advanced Shell Command Routing
                    if user_input.lower().startswith("cmd:"):
                        # Send to CMD shell
                        cmd_command = user_input[4:].strip()
                        print(f"🖥️  Executing in CMD: {cmd_command}")
                        result = subprocess.run(
                            cmd_command, shell=True, capture_output=True, text=True, cwd=self.cwd)
                        if result.returncode == 0:
                            print(f"✅ CMD Output:\n{result.stdout}")
                        else:
                            print(f"❌ CMD Error:\n{result.stderr}")
                        continue

                    elif user_input.lower().startswith("ps1:"):
                        # Send to PowerShell
                        ps1_command = user_input[4:].strip()
                        print(f"💻 Executing in PowerShell: {ps1_command}")
                        result = subprocess.run(
                            ["powershell", "-Command", ps1_command], capture_output=True, text=True, cwd=self.cwd)
                        if result.returncode == 0:
                            print(f"✅ PowerShell Output:\n{result.stdout}")
                        else:
                            print(f"❌ PowerShell Error:\n{result.stderr}")
                        continue

                    elif user_input.lower().startswith("bash:"):
                        # Send to Bash (if available)
                        bash_command = user_input[5:].strip()
                        print(f"🐧 Executing in Bash: {bash_command}")
                        try:
                            result = subprocess.run(
                                ["bash", "-c", bash_command], capture_output=True, text=True, cwd=self.cwd)
                            if result.returncode == 0:
                                print(f"✅ Bash Output:\n{result.stdout}")
                            else:
                                print(f"❌ Bash Error:\n{result.stderr}")
                        except FileNotFoundError:
                            print("❌ Bash not available on this system")
                        continue

                    elif user_input.lower().startswith("cs:"):
                        # Send to Cursor AI
                        cs_command = user_input[3:].strip()
                        print(f"🤖 Sending to Cursor AI: {cs_command}")
                        result = send_command_to_cursor(cs_command)
                        print(result)
                        continue

                    elif user_input.lower().startswith("deep:"):
                        # Deep research mode
                        research_topic = user_input[5:].strip()
                        print(f"🔬 Deep Research Mode: {research_topic}")
                        enhanced_prompt = f"Conduct deep research on: {research_topic}. Analyze thoroughly, find multiple sources, identify patterns, and provide comprehensive insights with actionable recommendations."
                        result = send_command_to_cursor(enhanced_prompt)
                        print(result)
                        continue

                    elif user_input.lower().startswith("review:"):
                        # Code review mode
                        review_target = user_input[7:].strip()
                        print(f"🔍 Code Review Mode: {review_target}")
                        enhanced_prompt = f"Review the code in {review_target}. Analyze for errors, bugs, security issues, performance problems, code quality, and suggest improvements. Be thorough and systematic."
                        result = send_command_to_cursor(enhanced_prompt)
                        print(result)
                        continue

                    elif user_input.lower().startswith("audit:"):
                        # Full project audit mode
                        audit_scope = user_input[6:].strip() if len(
                            user_input) > 6 else "entire project"
                        print(f"📊 Full Project Audit Mode: {audit_scope}")
                        enhanced_prompt = f"Conduct a comprehensive audit of the {audit_scope}. Review all code files systematically, identify errors, inconsistencies, integration issues, security vulnerabilities, performance bottlenecks, and architectural problems. Create a detailed report with prioritized fixes."
                        result = send_command_to_cursor(enhanced_prompt)
                        print(result)
                        continue

                    # Check if this should be a terminal command (not AI/Cursor related)
                    # Only execute as shell command if it's not a special command
                    is_special_command = any([
                        user_input.lower().startswith(("ai:", "cursor:", "chat:", "telegram:", "autopilot:", "theme", "config", "alias", "plugin")),
                        user_input.startswith('/'),
                        user_input.lower().startswith(("cmd:", "ps1:", "bash:", "cs:", "deep:", "review:", "audit:"))
                    ])
                    
                    if not is_special_command:
                        # This is a regular terminal command - execute it
                        result = self.shell_command(user_input)
                    else:
                        # This was handled by special command handlers above
                        continue

                    # Store result for potential use by other systems
                    self.last_command_result = result

                    # Send result to Telegram if controller is available
                    try:
                        from utils.telegram_controller import get_telegram_controller
                        telegram_controller = get_telegram_controller()
                        if telegram_controller:
                            # Format the result for Telegram
                            telegram_message = f"🔧 **CLI Command Result**\n\n"
                            telegram_message += f"**Command:** `{user_input}`\n\n"
                            telegram_message += f"**Result:**\n```\n{result}\n```"
                            
                            # Send to Telegram
                            telegram_controller._send_message(telegram_message)
                            print("📱 Result sent to Telegram")
                    except Exception as e:
                        print(f"⚠️  Failed to send result to Telegram: {e}")

                    # AUTOMATIC CLAPBACK - no need to ask!
                    if self.auto_clapback:
                        clapback = self.get_automatic_clapback(user_input)
                        print_with_effect(clapback, theme=self.current_theme)

                except KeyboardInterrupt:
                    print("\n⚠️  Use 'exit' to quit UwU-CLI")
                except EOFError:
                    break

        finally:
            # Save history
            try:
                readline.write_history_file(str(self.history_file))
            except:
                pass

            self.run_plugins_on_shutdown()

            # Send autopilot shutdown notification
            try:
                autopilot = get_autopilot()
                if autopilot and autopilot.enabled:
                    autopilot.notify_cli_exit()
            except Exception as e:
                print(f"⚠️  Autopilot notification failed: {e}")

            # Stop Telegram command control
            try:
                stop_telegram_control()
            except Exception as e:
                print(f"⚠️  Telegram control shutdown error: {e}")

            print("👋 UwU-CLI shutting down... stay sparkly~ ✨")

    def _handle_chat_commands(self, args):
        """Handle AI chat commands"""
        if not args:
            print("🤖 AI Chat Commands:")
            print("  chat:new <title>       - Start new AI conversation")
            print("  chat:list              - List all AI conversations")
            print("  chat:open <id>         - Open specific conversation")
            print("  chat:search <query>    - Search conversations")
            print("  chat:export <id>       - Export conversation")
            print("  chat:stats             - Show conversation statistics")
            return True

        subcommand = args[0].lower()

        try:
            from utils.ai_conversation_manager import get_conversation_manager
            manager = get_conversation_manager()

            if subcommand == "new":
                if len(args) < 2:
                    print("❌ Usage: chat:new <title>")
                    return True
                title = " ".join(args[1:])
                conv_id = manager.start_conversation(title)
                print(f"🤖 Started new conversation: {title}")
                print(f"📝 Conversation ID: {conv_id}")
                return True

            elif subcommand == "list":
                conversations = manager.list_conversations(limit=20)
                if conversations:
                    print(f"🤖 AI Conversations ({len(conversations)} total):")
                    print("-" * 60)
                    for conv in conversations:
                        created = conv.get('created_at', 'Unknown')[
                            :10]  # Just date
                        updated = conv.get('last_updated', 'Unknown')[:10]
                        messages = conv.get('message_count', 0)
                        tags = ", ".join(conv.get('tags', [])) if conv.get(
                            'tags') else "No tags"
                        print(f"📝 {conv['title']}")
                        print(
                            f"   ID: {conv['id'][:8]}... | Messages: {messages} | Created: {created} | Updated: {updated}")
                        if tags != "No tags":
                            print(f"   Tags: {tags}")
                        print()
                else:
                    print(
                        "🤖 No AI conversations found. Start one with: chat:new <title>")
                return True

            elif subcommand == "open":
                if len(args) < 2:
                    print("❌ Usage: chat:open <conversation_id>")
                    return True
                conv_id = args[1]
                conversation = manager.get_conversation(conv_id)
                if conversation:
                    print(f"🤖 Opening conversation: {conversation['title']}")
                    print("=" * 60)
                    for message in conversation.get('messages', []):
                        role = message['role'].upper()
                        # Format timestamp
                        timestamp = message['timestamp'][:19]
                        content = message['content']
                        print(f"[{timestamp}] {role}: {content}")
                        print()
                else:
                    print(f"❌ Conversation not found: {conv_id}")
                return True

            elif subcommand == "search":
                if len(args) < 2:
                    print("❌ Usage: chat:search <query>")
                    return True
                query = " ".join(args[1:])
                conversations = manager.search_conversations(query, limit=10)
                if conversations:
                    print(f"🔍 Search results for '{query}':")
                    print("-" * 60)
                    for conv in conversations:
                        created = conv.get('created_at', 'Unknown')[:10]
                        messages = conv.get('message_count', 0)
                        print(f"📝 {conv['title']}")
                        print(
                            f"   ID: {conv['id'][:8]}... | Messages: {messages} | Created: {created}")
                        print()
                else:
                    print(f"🔍 No conversations found matching '{query}'")
                return True

            elif subcommand == "export":
                if len(args) < 2:
                    print("❌ Usage: chat:export <conversation_id>")
                    return True
                conv_id = args[1]
                export_file = manager.export_conversation(conv_id, 'txt')
                if export_file:
                    print(f"💾 Conversation exported to: {export_file}")
                else:
                    print(f"❌ Failed to export conversation: {conv_id}")
                return True

            elif subcommand == "stats":
                stats = manager.get_statistics()
                print("📊 AI Conversation Statistics:")
                print("-" * 40)
                print(f"Total Conversations: {stats['total_conversations']}")
                print(f"Total Messages: {stats['total_messages']}")
                print(f"Total Tokens: {stats['total_tokens']}")
                print(f"Storage Size: {stats['storage_size_mb']} MB")

                if stats['most_used_tags']:
                    print("\n🏷️  Most Used Tags:")
                    for tag, count in stats['most_used_tags'][:5]:
                        print(f"  {tag}: {count}")

                if stats['recent_conversations']:
                    print("\n🕒 Recent Conversations:")
                    for conv in stats['recent_conversations'][:3]:
                        print(
                            f"  {conv['title']} ({conv['message_count']} messages)")
                return True

            else:
                print(f"❌ Unknown chat subcommand: {subcommand}")
                print(
                    "Use: chat:new, chat:list, chat:open, chat:search, chat:export, chat:stats")
                return True

        except ImportError:
            print("❌ AI Conversation Manager not available")
            return True
        except Exception as e:
            print(f"❌ Chat command error: {e}")
            return True

    def _handle_telegram_commands(self, args):
        """Handle Telegram control commands"""
        if not args:
            print("📱 Telegram Commands:")
            print("  telegram:enable    - Enable Telegram control")
            print("  telegram:disable   - Disable Telegram control")
            print("  telegram:status    - Check Telegram status")
            print("  telegram:restart   - Restart Telegram control")
            return True

        subcommand = args[0].lower()

        if subcommand == "enable":
            self.config["telegram_enabled"] = True
            save_config(self.config)
            print("✅ Telegram enabled - restart UwU-CLI to activate")
            return True

        elif subcommand == "disable":
            self.config["telegram_enabled"] = False
            save_config(self.config)
            print("❌ Telegram disabled - restart UwU-CLI to deactivate")
            return True

        elif subcommand == "status":
            telegram_enabled = self.config.get("telegram_enabled", True)
            print(
                f"📱 Telegram Status: {'Enabled' if telegram_enabled else 'Disabled'}")
            return True

        elif subcommand == "restart":
            print("🔄 Telegram restart - restart UwU-CLI to apply changes")
            return True

        else:
            print(f"❌ Unknown telegram subcommand: {subcommand}")
            print(
                "Use: telegram:enable, telegram:disable, telegram:status, telegram:restart")
            return True


# ------------------------------
# Main Entry Point
# ------------------------------
def main():
    """Main entry point"""
    try:
        cli = UwUCLI()
        cli.start()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
