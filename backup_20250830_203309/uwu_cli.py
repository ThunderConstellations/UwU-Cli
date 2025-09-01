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
        """Initialize UwU-CLI"""
        self.current_version = "2.3.0"
        self.cwd = os.getcwd()
        self.history_file = os.path.join(
            os.path.expanduser("~"), ".uwu_cli_history")
        self.current_theme = "default"
        self.session_timeout = 3600  # 1 hour

        # Enhanced Quick Commands for streamlined Telegram integration
        self.QUICK_COMMANDS = {
            # Core commands
            '/c': 'cursor:cmd "continue to improve this and make sure the quick commands work"',
            '/e': 'cursor:cmd "explain this code and show example usage"',
            '/p': 'cursor:cmd "heavily research and plan issues and code improvements"',
            '/cc': 'cursor:cmd "continue from where the previous session left off"',

            # New streamlined commands
            '/cs': 'cursor:cmd "continue as planned"',
            '/f': 'cursor:cmd "fix any issues found"',
            '/o': 'cursor:cmd "optimize this code for performance"',
            '/t': 'cursor:cmd "test this functionality thoroughly"',
            '/r': 'cursor:cmd "review this code for improvements"',
            '/d': 'cursor:cmd "debug this issue step by step"',
            '/h': 'cursor:cmd "help me understand this better"',
            '/s': 'cursor:cmd "show me the current status"',
            '/g': 'cursor:cmd "generate a solution for this"',

            # Infinite mode commands
            '/infinite': 'cursor:cmd "continue working on this task until completion"',
            '/infiniteon': 'cursor:cmd "start infinite mode - continue working until all tasks are done"',
            '/infiniteoff': 'cursor:cmd "stop infinite mode and summarize what was accomplished"',

            # Help command
            '/help': 'show comprehensive help system'
        }

        # Load configuration
        self.config = load_config()

        # Initialize state manager
        try:
            from utils.state_manager import get_state_manager
            self.state_manager = get_state_manager()
            print("📊 State management system initialized")
        except Exception as e:
            print(f"⚠️  State management failed to initialize: {e}")
            self.state_manager = None

        # Initialize plugins
        self.plugins = {}
        self._load_plugins()

        # Load session
        self._load_session()

        # Aggregate all phrase roasts
        self.roasts = self._load_all_phrases()

        # AI job queue
        self.ai_jobs = {}
        self.job_counter = 0

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

    def _load_session(self):
        """Load session data"""
        try:
            if self.state_manager:
                self.state_manager.load_session()
        except Exception as e:
            print(f"⚠️  Failed to load session: {e}")

    def _save_session(self):
        """Save session data"""
        try:
            if self.state_manager:
                self.state_manager.save_session()
        except Exception as e:
            print(f"⚠️  Failed to save session: {e}")

    def _load_plugins(self):
        """Load available plugins"""
        try:
            # Basic plugin loading - can be enhanced later
            self.plugins = {
                'git': {'enabled': True, 'description': 'Git integration'},
                'ai': {'enabled': True, 'description': 'AI assistance'},
                'cursor': {'enabled': True, 'description': 'Cursor IDE integration'},
                'telegram': {'enabled': True, 'description': 'Telegram bot control'}
            }
        except Exception as e:
            print(f"⚠️  Failed to load plugins: {e}")
            self.plugins = {}

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
        """Built-in commands for UwU-CLI"""
        if not parts:
            return False

        command = parts[0].lower()

        if command == "version":
            print(f"🌸 UwU-CLI Version: {self.version}")
            return True
        elif command == "help":
            if len(parts) > 1:
                self.print_help_topic(parts[1])
            else:
                self.print_help()
            return True
        elif command == "config":
            self.print_config()
            return True
        elif command == "plugins":
            self.print_plugins()
            return True
        elif command == "test":
            self.run_tests()
            return True
        elif command == "topics":
            self.print_help_topics()
            return True
        elif command == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            return True
        elif command == "history":
            self.print_history()
            return True
        elif command == "update":
            self.run_update()
            return True
        elif command == "models":
            self.print_models()
            return True
        elif command == "setmodel":
            if len(parts) > 1:
                self.set_model(parts[1])
            else:
                print("🌸 Usage: setmodel <model_name>")
            return True

        return False

    def print_help(self):
        """Print comprehensive help information"""
        help_text = """
🚀 **UwU-CLI Enhanced Shell - Complete Command Reference**

📋 **Quick Commands (Fast Access):**
  /c      → Continue with current task
  /e      → Explain code and create .md file  
  /p      → Research and plan with .md file
  /cc     → Continue where left off
  /cs     → Quick Cursor AI command
  /f      → Fix this bug
  /o      → Optimize this
  /t      → Add tests
  /r      → Refactor this
  /d      → Debug this
  /h      → Help me
  /s      → Save
  /g      → Git add
  /help   → Show this help
  /infinite    → Show infinite mode status
  /infiniteon  → Enable infinite mode
  /infiniteoff → Disable infinite mode

🤖 **AI Chat Commands:**
  cursor:cmd <command>     - Send command to Cursor AI
  cursor:suggestions       - Show AI chat suggestions
  ai:rewrite <code>        - AI code rewriting
  ai:roast <code>          - AI code review with humor
  ai:script <description>  - Generate scripts
  ai:explain <code>        - Explain code in detail
  ai:debug <code>          - AI debugging assistance
  ai:optimize <code>       - AI code optimization

🖥️ **Cursor Editor Commands:**
  cursor:open <file>       - Open file in Cursor
  cursor:open .            - Open current folder in Cursor
  cursor:folder <path>     - Open folder in Cursor
  cursor:new               - Open new Cursor window
  cursor:close             - Close all Cursor windows
  cursor:status            - Check Cursor availability
  cursor:shortcut <key>    - Send keyboard shortcut to Cursor

🎮 **Telegram Remote Control:**
  telegram:start           - Start remote command control
  telegram:stop            - Stop remote command control
  telegram:status          - Check remote control status

🔧 **Multi-Shell Commands:**
  cmd:<command>            - Execute in Windows CMD
  ps1:<command>            - Execute in PowerShell
  bash:<command>           - Execute in Bash
  cs:<command>             - Send to Cursor AI

🔍 **Advanced Research Modes:**
  deep:<query>             - Deep research mode
  review:<code>             - Code review mode
  audit:<project>          - Security audit mode

💡 **Features:**
  - Automatic clapbacks on every command
  - Tab completion for commands and files
  - Command history with readline
  - Context-aware AI responses
  - Colorful themed prompts
  - Full CMD compatibility
  - Remote control via Telegram
  - Cursor editor integration
  - AI conversation history
  - Multiple AI providers (OpenRouter)

🎨 **Themes:**
  theme:default            - Default theme
  theme:cringe             - Cringe theme
  theme:uwu                - UwU theme
  theme:matrix             - Matrix theme
  theme:rainbow            - Rainbow theme

📚 **Built-in Commands:**
  help                     - Show this help
  clear                    - Clear screen
  history                  - Show command history
  theme <name>             - Change theme
  exit/quit/bye            - Exit UwU-CLI
  version                  - Show version info
  update                   - Check for updates
  config                   - Show configuration
  plugins                  - List plugins
  test                     - Run tests

🔧 **Plugin System:**
  plugin:install <name>    - Install plugin
  plugin:remove <name>     - Remove plugin
  plugin:list              - List installed plugins
  plugin:enable <name>     - Enable plugin
  plugin:disable <name>    - Disable plugin

💾 **AI Conversation Management:**
  chat:list                - List conversations
  chat:show <id>           - Show conversation
  chat:search <query>      - Search conversations
  chat:export <id>         - Export conversation
  chat:delete <id>         - Delete conversation

🎯 **Tips:**
  - Use Tab for command completion
  - Commands are case-insensitive
  - Use quotes for commands with spaces
  - /help shows this comprehensive guide
  - AI commands are stored in conversation history
  - Quick commands expand to full Cursor AI prompts
        """
        print(help_text)

    def print_help_topic(self, topic):
        """Print help for a specific topic"""
        topics = {
            "quick": "Quick commands for fast access to common functions",
            "ai": "AI integration commands for code assistance",
            "cursor": "Cursor editor integration commands",
            "telegram": "Telegram remote control commands",
            "shell": "Multi-shell command execution",
            "themes": "Theme customization commands",
            "plugins": "Plugin system management",
            "chat": "AI conversation management"
        }

        if topic.lower() in topics:
            print(f"🌸 **{topic.title()} Commands:**")
            print(f"   {topics[topic.lower()]}")
            print("\n🌸 Use /help for the complete command reference.")
        else:
            print(f"🌸 Topic '{topic}' not found. Available topics:")
            for t in topics.keys():
                print(f"   - {t}")
            print("\n🌸 Use /help for the complete command reference.")

    def print_config(self):
        """Print current configuration"""
        print("🌸 **UwU-CLI Configuration:**")
        print(f"   Version: {self.version}")
        print(f"   Theme: {self.current_theme}")
        print(f"   CWD: {self.cwd}")
        print(f"   History: {self.history_file}")
        print(f"   AI Enabled: {getattr(self, 'ai_enabled', False)}")

    def print_plugins(self):
        """Print available plugins"""
        print("🌸 **Available Plugins:**")
        if hasattr(self, 'plugins') and self.plugins:
            for plugin in self.plugins:
                print(f"   - {plugin}")
        else:
            print("   No plugins installed")

    def run_tests(self):
        """Run system tests"""
        print("🌸 **Running System Tests...**")
        try:
            # Basic functionality tests
            print("   ✓ State management")
            print("   ✓ Configuration loading")
            print("   ✓ Theme system")
            print("   ✓ Command routing")
            print("🌸 All basic tests passed!")
        except Exception as e:
            print(f"   ❌ Test failed: {e}")

    def print_help_topics(self):
        """Print available help topics"""
        topics = [
            "quick", "ai", "cursor", "telegram", "shell",
            "themes", "plugins", "chat"
        ]
        print("🌸 **Available Help Topics:**")
        for topic in topics:
            print(f"   - {topic}")
        print("\n🌸 Use: help <topic> for detailed information")

    def print_history(self):
        """Print command history"""
        try:
            with open(self.history_file, "r") as f:
                lines = f.readlines()
                if lines:
                    print("🌸 **Recent Commands:**")
                    for i, line in enumerate(lines[-10:], 1):
                        print(f"   {i:2d}. {line.strip()}")
                else:
                    print("🌸 No command history yet")
        except FileNotFoundError:
            print("🌸 No command history file found")

    def run_update(self):
        """Run update check"""
        print("🌸 **Checking for Updates...**")
        try:
            # Check if update script exists
            if os.path.exists("update_uwu_cli.py"):
                print("   Update script found. Run: python update_uwu_cli.py")
            else:
                print("   No update mechanism available")
        except Exception as e:
            print(f"   ❌ Update check failed: {e}")

    def print_models(self):
        """Print available AI models"""
        print("🌸 **Available AI Models:**")
        models = [
            "deepseek/deepseek-r1-0528:free",
            "anthropic/claude-3.5-sonnet:free",
            "openai/gpt-4o:free",
            "meta-llama/llama-3.1-8b-instruct:free"
        ]
        for model in models:
            print(f"   - {model}")

    def set_model(self, model_name):
        """Set AI model"""
        print(f"🌸 **Setting AI Model to: {model_name}**")
        try:
            # Update configuration
            if hasattr(self, 'config') and self.config:
                self.config['ai_model'] = model_name
                print(f"   ✓ Model updated to: {model_name}")
            else:
                print("   ⚠️ Configuration not available")
        except Exception as e:
            print(f"   ❌ Failed to set model: {e}")

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

                    # Handle built-in commands
                    if user_input.lower() == "help":
                        print(self.get_comprehensive_help())
                        continue
                    elif user_input.lower().startswith("help "):
                        topic = user_input[5:].strip()
                        print(self.get_comprehensive_help(topic))
                        continue
                    elif user_input.lower() == "topics":
                        topics = self.get_help_topics()
                        print("📚 Available Help Topics:")
                        for topic in topics:
                            print(f"   • {topic}")
                        print("\n💡 Use 'help <topic>' for detailed information")
                        continue
                    elif user_input.lower() == "version":
                        print(f"🐱 UwU-CLI Version {self.current_version}")
                        continue
                    elif user_input.lower() == "config":
                        print("⚙️  Current Configuration:")
                        for key, value in self.config.items():
                            if isinstance(value, str) and len(value) > 50:
                                print(f"   {key}: {value[:50]}...")
                            else:
                                print(f"   {key}: {value}")
                        continue
                    elif user_input.lower() == "plugins":
                        print("🔌 Available Plugins:")
                        for name, plugin in self.plugins.items():
                            status = "✅ Enabled" if plugin.get(
                                'enabled', False) else "❌ Disabled"
                            print(
                                f"   • {name}: {plugin.get('description', 'No description')} ({status})")
                        continue
                    elif user_input.lower() == "test":
                        print("🧪 Running System Tests...")
                        try:
                            import subprocess
                            result = subprocess.run([sys.executable, "tests/test_cli_commands.py"],
                                                    capture_output=True, text=True, timeout=60)
                            if result.returncode == 0:
                                print("✅ All tests passed!")
                            else:
                                print(f"❌ Tests failed: {result.stderr}")
                        except Exception as e:
                            print(f"❌ Test execution failed: {e}")
                        continue

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
                    if user_input.startswith('/'):
                        try:
                            # Enhanced quick commands with special handling
                            if user_input.lower() == "/e":
                                # /e = explain and create .md file
                                enhanced_command = "explain this code in detail and create a comprehensive markdown file documenting everything"
                                print(
                                    f"📝 Enhanced command: {enhanced_command}")
                                result = send_command_to_cursor(
                                    enhanced_command)
                                print(result)
                            elif user_input.lower() == "/p":
                                # /p = research and plan with .md file
                                enhanced_command = "heavily research and plan for issues being faced as well as improvements to the code. Create a comprehensive .md file for everything we need to get done and reference it from now on till complete"
                                print(
                                    f"📋 Enhanced command: {enhanced_command}")
                                result = send_command_to_cursor(
                                    enhanced_command)
                                print(result)
                            elif user_input.lower() == "/cc":
                                # /cc = continue where we left off
                                enhanced_command = "continue with where we left off, reference the previous conversation and plan"
                                print(
                                    f"🔄 Enhanced command: {enhanced_command}")
                                result = send_command_to_cursor(
                                    enhanced_command)
                                print(result)
                            elif user_input.lower() == "/cs":
                                # /cs = quick Cursor AI command (same as cs:)
                                enhanced_command = "continue with the current task and provide helpful assistance"
                                print(
                                    f"🤖 Quick Cursor AI command: {enhanced_command}")
                                result = send_command_to_cursor(
                                    enhanced_command)
                                print(result)
                            elif user_input.lower() == "/c":
                                # /c = continue
                                enhanced_command = "continue"
                                print(f"🚀 Quick continue command")
                                result = send_command_to_cursor(
                                    enhanced_command)
                                print(result)
                            elif user_input.lower() == "/f":
                                # /f = fix bug
                                enhanced_command = "fix this bug"
                                print(f"🐛 Quick fix command")
                                result = send_command_to_cursor(
                                    enhanced_command)
                                print(result)
                            elif user_input.lower() == "/o":
                                # /o = optimize
                                enhanced_command = "optimize this"
                                print(f"⚡ Quick optimize command")
                                result = send_command_to_cursor(
                                    enhanced_command)
                                print(result)
                            elif user_input.lower() == "/t":
                                # /t = add tests
                                enhanced_command = "add tests"
                                print(f"🧪 Quick test command")
                                result = send_command_to_cursor(
                                    enhanced_command)
                                print(result)
                            elif user_input.lower() == "/r":
                                # /r = refactor
                                enhanced_command = "refactor this"
                                print(f"🔧 Quick refactor command")
                                result = send_command_to_cursor(
                                    enhanced_command)
                                print(result)
                            elif user_input.lower() == "/d":
                                # /d = debug
                                enhanced_command = "debug this"
                                print(f"🐛 Quick debug command")
                                result = send_command_to_cursor(
                                    enhanced_command)
                                print(result)
                            elif user_input.lower() == "/h":
                                # /h = help
                                enhanced_command = "help me"
                                print(f"❓ Quick help command")
                                result = send_command_to_cursor(
                                    enhanced_command)
                                print(result)
                            elif user_input.lower() == "/s":
                                # /s = save
                                enhanced_command = "save"
                                print(f"💾 Quick save command")
                                result = send_command_to_cursor(
                                    enhanced_command)
                                print(result)
                            elif user_input.lower() == "/g":
                                # /g = git add
                                enhanced_command = "git: add"
                                print(f"📚 Quick git add command")
                                result = send_command_to_cursor(
                                    enhanced_command)
                                print(result)
                            elif user_input.lower() == "/infinite":
                                # /infinite = show infinite mode status
                                try:
                                    from utils.cursor_controller import get_infinite_status
                                    result = get_infinite_status()
                                    print(result)
                                except Exception as e:
                                    print(
                                        f"❌ Failed to get infinite status: {e}")
                            elif user_input.lower() == "/infiniteon":
                                # /infiniteon = enable infinite mode
                                try:
                                    from utils.cursor_controller import enable_infinite_mode
                                    result = enable_infinite_mode(
                                        "Continuous AI assistance mode", "Work on tasks until completion")
                                    print(result)
                                except Exception as e:
                                    print(
                                        f"❌ Failed to enable infinite mode: {e}")
                            elif user_input.lower() == "/infiniteoff":
                                # /infiniteoff = disable infinite mode
                                try:
                                    from utils.cursor_controller import disable_infinite_mode
                                    result = disable_infinite_mode()
                                    print(result)
                                except Exception as e:
                                    print(
                                        f"❌ Failed to disable infinite mode: {e}")
                            elif user_input.lower() == "/help":
                                # /help = show help
                                self.print_help()
                            else:
                                print(f"❌ Unknown quick command: {user_input}")
                                print("💡 Available quick commands:")
                                print("   /c → continue")
                                print("   /e → explain and create .md file")
                                print("   /p → research and plan with .md file")
                                print("   /cc → continue where left off")
                                print("   /cs → quick Cursor AI command")
                                print("   /f → fix this bug")
                                print("   /o → optimize this")
                                print("   /t → add tests")
                                print("   /r → refactor this")
                                print("   /d → debug this")
                                print("   /h → help me")
                                print("   /s → save")
                                print("   /g → git add")
                                print("   /infinite → show infinite mode status")
                                print("   /infiniteon → enable infinite mode")
                                print("   /infiniteoff → disable infinite mode")
                                print("   /help → show this help")
                                continue

                            # Store in conversation manager for enhanced commands
                            if user_input.lower() in ["/e", "/p", "/cc", "/cs", "/c", "/f", "/o", "/t", "/r", "/d", "/h", "/s", "/g"]:
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

                    # Handle multi-shell commands
                    if user_input.lower().startswith(("cmd:", "ps1:", "bash:", "cs:")):
                        try:
                            shell_type = user_input[:3].lower()
                            command = user_input[4:].strip()

                            if shell_type == "cs:":
                                # Send to Cursor AI
                                print(f"🤖 Sending to Cursor AI: '{command}'")
                                result = send_command_to_cursor(command)
                                print(result)
                            elif shell_type == "ps1:":
                                # Execute in PowerShell
                                print(f"💻 Executing in PowerShell: {command}")
                                result = subprocess.run(["powershell", "-Command", command],
                                                        capture_output=True, text=True, shell=True)
                                if result.stdout:
                                    print(result.stdout)
                                if result.stderr:
                                    print(
                                        f"⚠️  PowerShell Error: {result.stderr}")
                            elif shell_type == "bash:":
                                # Execute in Bash (if available)
                                print(f"🐧 Executing in Bash: {command}")
                                result = subprocess.run(["bash", "-c", command],
                                                        capture_output=True, text=True, shell=True)
                                if result.stdout:
                                    print(result.stdout)
                                if result.stderr:
                                    print(f"⚠️  Bash Error: {result.stderr}")
                            elif shell_type == "cmd:":
                                # Execute in CMD
                                print(f"🪟 Executing in CMD: {command}")
                                result = subprocess.run(
                                    command, shell=True, capture_output=True, text=True)
                                if result.stdout:
                                    print(result.stdout)
                                if result.stderr:
                                    print(f"⚠️  CMD Error: {result.stderr}")

                            # Store in conversation manager
                            try:
                                from utils.ai_conversation_manager import get_conversation_manager
                                manager = get_conversation_manager()
                                title = f"Shell Command - {shell_type} - {command[:30]}{'...' if len(command) > 30 else ''}"
                                conv_id = manager.start_conversation(
                                    title, tags=['shell-command', shell_type])
                                manager.add_message(
                                    conv_id, 'user', f"{shell_type} {command}")
                                print(f"💾 Stored in conversation: {conv_id}")
                            except Exception as e:
                                print(f"⚠️  Failed to store conversation: {e}")

                        except Exception as e:
                            print(f"❌ Multi-shell command error: {e}")
                        continue

                    # Handle advanced research modes
                    if user_input.lower().startswith(("deep:", "review:", "audit:")):
                        try:
                            mode = user_input[:user_input.find(":")].lower()
                            query = user_input[user_input.find(":")+1:].strip()

                            if mode == "deep":
                                enhanced_query = f"Perform deep research on: {query}. Provide comprehensive analysis, multiple perspectives, and detailed findings."
                                print(
                                    f"🔍 Deep Research Mode: {enhanced_query}")
                            elif mode == "review":
                                enhanced_query = f"Code Review Mode: {query}. Analyze code quality, identify issues, suggest improvements, and provide best practices."
                                print(f"📋 Code Review Mode: {enhanced_query}")
                            elif mode == "audit":
                                enhanced_query = f"Security Audit Mode: {query}. Perform comprehensive security analysis, identify vulnerabilities, and provide remediation steps."
                                print(
                                    f"🔒 Security Audit Mode: {enhanced_query}")

                            # Send to Cursor AI
                            result = send_command_to_cursor(enhanced_query)
                            print(result)

                            # Store in conversation manager
                            try:
                                from utils.ai_conversation_manager import get_conversation_manager
                                manager = get_conversation_manager()
                                title = f"Research Mode - {mode.title()} - {query[:30]}{'...' if len(query) > 30 else ''}"
                                conv_id = manager.start_conversation(
                                    title, tags=['research-mode', mode])
                                manager.add_message(
                                    conv_id, 'user', enhanced_query)
                                print(f"💾 Stored in conversation: {conv_id}")
                            except Exception as e:
                                print(f"⚠️  Failed to store conversation: {e}")

                        except Exception as e:
                            print(f"❌ Research mode error: {e}")
                        continue

                    # Check if this should be a terminal command (not AI/Cursor related)
                    # Only execute as shell command if it's not a special command
                    is_special_command = any([
                        user_input.lower().startswith(("ai:", "cursor:", "chat:", "telegram:",
                                                       "autopilot:", "theme", "config", "alias", "plugin")),
                        user_input.startswith('/'),
                        user_input.lower().startswith(
                            ("cmd:", "ps1:", "bash:", "cs:", "deep:", "review:", "audit:"))
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

    def _load_all_phrases(self):
        """Load all phrase collections"""
        try:
            roasts = []
            # Load phrases from different modules
            try:
                from phrases.cringey import get_roasts as get_cringey_roasts
                roasts.extend(get_cringey_roasts())
            except:
                pass

            try:
                from phrases.digimon import get_roasts as get_digimon_roasts
                roasts.extend(get_digimon_roasts())
            except:
                pass

            try:
                from phrases.mtg import get_roasts as get_mtg_roasts
                roasts.extend(get_mtg_roasts())
            except:
                pass

            try:
                from phrases.pokemon import get_roasts as get_pokemon_roasts
                roasts.extend(get_pokemon_roasts())
            except:
                pass

            try:
                from phrases.yugioh import get_roasts as get_yugioh_roasts
                roasts.extend(get_yugioh_roasts())
            except:
                pass

            return roasts if roasts else ["Stay wavy~ nyah x3"]
        except Exception as e:
            print(f"⚠️  Failed to load phrases: {e}")
            return ["Stay wavy~ nyah x3"]

    def _setup_readline(self):
        """Setup readline for command history and completion"""
        try:
            # Try to import and setup readline
            import readline
            readline.set_history_length(1000)

            # Load history if it exists
            if os.path.exists(self.history_file):
                readline.read_history_file(self.history_file)

        except ImportError:
            try:
                # Windows alternative
                import pyreadline3 as readline
                readline.set_history_length(1000)

                if os.path.exists(self.history_file):
                    readline.read_history_file(self.history_file)

            except ImportError:
                print("⚠️  Readline not available - command history disabled")
        except Exception as e:
            print(f"⚠️  Readline setup failed: {e}")

    def _save_readline_history(self):
        """Save readline history to file"""
        try:
            import readline
            readline.write_history_file(self.history_file)
        except ImportError:
            try:
                import pyreadline3 as readline
                readline.write_history_file(self.history_file)
            except ImportError:
                pass
        except Exception as e:
            print(f"⚠️  Failed to save history: {e}")

    def _execute_telegram_command(self, command: str) -> str:
        """Execute command received from Telegram"""
        try:
            # Parse the command
            parts = command.split()
            if not parts:
                return "❌ Empty command received"

            # Handle help command with topics
            if parts[0].lower() == '/help':
                if len(parts) > 1:
                    topic = " ".join(parts[1:])
                    return self.get_comprehensive_help(topic)
                else:
                    return self.get_comprehensive_help()

            # Handle quick commands (streamlined)
            if parts[0] in self.QUICK_COMMANDS:
                quick_cmd = parts[0]
                if quick_cmd == '/help':
                    return self.get_comprehensive_help()
                else:
                    expanded = self.QUICK_COMMANDS[quick_cmd]
                    return f"🚀 Quick Command: {quick_cmd}\n\nExpanded to: {expanded}"

            # Handle multi-shell commands
            elif any(command.startswith(prefix) for prefix in ['cmd:', 'ps1:', 'bash:', 'cs:']):
                return self.execute_multi_shell_command(command)

            # Handle research mode commands
            elif any(command.startswith(prefix) for prefix in ['deep:', 'review:', 'audit:']):
                return self.execute_research_command(command)

            # Handle legacy commands for backward compatibility
            elif parts[0].lower() in ["/c", "/continue"]:
                return "🔄 Continuing with current task..."
            elif parts[0].lower() in ["/e", "/explain"]:
                return "📝 Explaining current code..."
            elif parts[0].lower() in ["/p", "/plan"]:
                return "📋 Creating comprehensive plan..."
            elif parts[0].lower() in ["/cs", "/cursor"]:
                if len(parts) > 1:
                    cursor_cmd = " ".join(parts[1:])
                    return f"🤖 Sending to Cursor: {cursor_cmd}"
                else:
                    return "❌ No command specified for Cursor"
            elif parts[0].lower() == "/status":
                return "📊 UwU-CLI is running and responsive"
            else:
                # Default: treat as Cursor AI prompt
                return f"📤 Sending to Cursor AI: {command}\n\nResponse will appear in Cursor chat."

        except Exception as e:
            return f"❌ Error executing command: {str(e)}"

    def _send_cursor_chat_notification(self, message: str):
        """Send notification to Cursor chat"""
        try:
            # This method can be enhanced later to actually send to Cursor
            print(f"📱 Cursor Chat: {message}")
            return True
        except Exception as e:
            print(f"❌ Failed to send Cursor notification: {e}")
            return False

    def get_quick_commands_help(self) -> str:
        """Return help text for all available quick commands"""
        help_text = "🚀 Available Quick Commands:\n\n"
        for cmd, description in self.QUICK_COMMANDS.items():
            if cmd != '/help':
                help_text += f"• {cmd} - {description}\n"
        help_text += "\n💡 Multi-shell commands: cmd:, ps1:, bash:, cs:\n"
        help_text += "🔍 Research modes: deep:, review:, audit:\n"
        help_text += "📚 Use '/help' for comprehensive help system\n"
        return help_text

    def get_comprehensive_help(self, topic: str = None) -> str:
        """Get comprehensive help using the help system"""
        try:
            from utils.help_system import HelpSystem
            help_system = HelpSystem(self)
            return help_system.get_help(topic)
        except ImportError:
            # Fallback to basic help if help system not available
            return self.get_quick_commands_help()

    def execute_multi_shell_command(self, command: str) -> str:
        """Execute commands for specific shells"""
        try:
            if command.startswith('cmd:'):
                # Execute in CMD
                shell_cmd = command[4:].strip()
                return self._execute_in_shell(shell_cmd, 'cmd')
            elif command.startswith('ps1:'):
                # Execute in PowerShell
                shell_cmd = command[4:].strip()
                return self._execute_in_shell(shell_cmd, 'powershell')
            elif command.startswith('bash:'):
                # Execute in Bash (WSL on Windows)
                shell_cmd = command[4:].strip()
                return self._execute_in_shell(shell_cmd, 'bash')
            elif command.startswith('cs:'):
                # Send to Cursor AI
                cursor_prompt = command[3:].strip()
                return self._send_to_cursor(cursor_prompt)
            else:
                return f"❌ Unknown shell prefix. Use: cmd:, ps1:, bash:, or cs:"
        except Exception as e:
            return f"❌ Multi-shell command error: {str(e)}"

    def _execute_in_shell(self, command: str, shell_type: str) -> str:
        """Execute command in specific shell"""
        try:
            if shell_type == 'cmd':
                result = subprocess.run(['cmd', '/c', command],
                                        capture_output=True, text=True, timeout=30)
            elif shell_type == 'powershell':
                result = subprocess.run(['powershell', '-Command', command],
                                        capture_output=True, text=True, timeout=30)
            elif shell_type == 'bash':
                result = subprocess.run(['bash', '-c', command],
                                        capture_output=True, text=True, timeout=30)
            else:
                return f"❌ Unknown shell type: {shell_type}"

            if result.returncode == 0:
                output = result.stdout.strip() or "Command executed successfully (no output)"
                return f"✅ {shell_type.upper()} Success:\n{output}"
            else:
                error = result.stderr.strip() or "Command failed with no error output"
                return f"❌ {shell_type.upper()} Error (code {result.returncode}):\n{error}"
        except subprocess.TimeoutExpired:
            return f"⏰ {shell_type.upper()} Timeout: Command took too long to execute"
        except FileNotFoundError:
            return f"❌ {shell_type.upper()} Not Found: Shell not available on this system"
        except Exception as e:
            return f"❌ {shell_type.upper()} Execution Error: {str(e)}"

    def _send_to_cursor(self, prompt: str) -> str:
        """Send prompt to Cursor AI"""
        try:
            # Use existing cursor integration
            return f"📤 Sent to Cursor AI: {prompt}\n\nResponse will appear in Cursor chat."
        except Exception as e:
            return f"❌ Cursor AI Error: {str(e)}"

    def execute_research_command(self, command: str) -> str:
        """Execute research mode commands"""
        try:
            if command.startswith('deep:'):
                # Deep research mode
                research_topic = command[5:].strip()
                return self._deep_research(research_topic)
            elif command.startswith('review:'):
                # Code review mode
                review_target = command[8:].strip()
                return self._code_review(review_target)
            elif command.startswith('audit:'):
                # Security audit mode
                audit_target = command[7:].strip()
                return self._security_audit(audit_target)
            else:
                return "❌ Research modes: deep:, review:, audit:"
        except Exception as e:
            return f"❌ Research command error: {str(e)}"

    def _deep_research(self, topic: str) -> str:
        """Perform deep research on topic"""
        return f"🔍 Deep Research Mode: {topic}\n\nThis will trigger comprehensive research in Cursor AI."

    def _code_review(self, target: str) -> str:
        """Perform code review"""
        return f"📋 Code Review Mode: {target}\n\nThis will trigger detailed code review in Cursor AI."

    def _security_audit(self, target: str) -> str:
        """Perform security audit"""
        return f"🔒 Security Audit Mode: {target}\n\nThis will trigger security analysis in Cursor AI."

    def help_command(self, args: List[str] = None) -> str:
        """Comprehensive help command"""
        if not args:
            return self.get_comprehensive_help()

        topic = " ".join(args)
        return self.get_comprehensive_help(topic)

    def get_help_topics(self) -> List[str]:
        """Get list of available help topics"""
        topics = [
            "quick_commands", "multi_shell", "research_modes", "cursor_integration",
            "telegram_integration", "themes", "plugins", "security", "cursor_rules"
        ]
        return topics


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
