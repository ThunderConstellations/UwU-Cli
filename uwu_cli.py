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

        # Setup readline for autosuggestions
        self._setup_readline()

        print("UwU-CLI CMD replacement activated! Stay wavy~ nyah x3")

    def _setup_readline(self):
        """Setup readline for autosuggestions and history"""
        try:
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

        # Command completions
        if not text or text.startswith(' '):
            # Show common commands
            common_cmds = ['uwu', 'ai:rewrite', 'ai:roast',
                           'theme', 'config', 'help', 'exit']
            completions.extend(
                [cmd for cmd in common_cmds if cmd.startswith(text.lstrip())])

        # File completions
        if text and not text.startswith(' '):
            # Try to complete files/directories
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
            # Update working directory
            if cmd.startswith("cd "):
                new_dir = cmd[3:].strip()
                if new_dir == "~":
                    new_dir = str(Path.home())
                os.chdir(new_dir)
                self.cwd = os.getcwd()
                print(f"📁 Changed directory to: {self.cwd}")
            else:
                # Execute other commands with CMD enhancements
                result = self.cmd_enhancer.execute_command(cmd, cwd=self.cwd)
                if result:
                    print(result)

        except Exception as e:
            print(f"❌ Shell command error: {e}")

    def handle_aliases(self, user_input):
        """Handle command aliases"""
        parts = user_input.split()
        if not parts:
            return user_input

        alias_cmd = parts[0]
        resolved = get_alias(alias_cmd)
        if resolved:
            return resolved + " " + " ".join(parts[1:])
        return user_input

    def builtin_commands(self, parts):
        """Handle built-in UwU-CLI commands"""
        cmd = parts[0]
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

💡 Features:
  - Automatic clapbacks on every command
  - Tab completion for commands and files
  - Command history with readline
  - Context-aware AI responses
  - Colorful themed prompts
  - Full CMD compatibility
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

                    # Execute shell command
                    self.shell_command(user_input)

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
            print("👋 UwU-CLI shutting down... stay sparkly~ ✨")


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
