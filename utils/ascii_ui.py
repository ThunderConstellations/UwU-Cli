"""
Animated ASCII UI module for UwU-CLI using Rich
Provides spinners, themed effects, and visual feedback
"""

import sys
import os
import random
import time
from typing import Optional, List, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.theme import Theme
from rich.text import Text

# Initialize Rich Console with a custom theme
custom_theme = Theme({
    "uwu": "magenta",
    "feral": "bold red",
    "wizard": "bright_cyan",
    "emo": "dim white",
    "rainbow": "yellow",
    "neon": "cyan",
    "pastel": "bright_magenta",
    "toxic": "bold green",
    "info": "blue",
    "warning": "yellow",
    "error": "bold red",
    "success": "green"
})

console = Console(theme=custom_theme)

class Spinner:
    """Rich-based non-blocking spinner"""
    def __init__(self, text="Loading", theme="uwu"):
        self.text = text
        self.theme = theme
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[{task.description}]"),
            transient=True,
            console=console
        )
        self._task = None

    def start(self):
        self._progress.start()
        self._task = self._progress.add_task(description=self.text)

    def stop(self):
        if self._task is not None:
            self._progress.stop()

def print_with_effect(text: str, effect: Optional[str] = None, theme: str = "uwu"):
    """Print text inside a themed Rich panel"""
    style = theme if theme in custom_theme.styles else "uwu"
    title = f"UwU [{theme}]"

    display_text = text
    if effect:
        display_text = f"{text}\n\n[dim italic]Effect: {effect}[/]"

    console.print(Panel(display_text, title=title, border_style=style))

def get_colored_prompt(theme_name: str, cwd: str = "") -> str:
    """Get a colorful themed prompt string (using ANSI for input compatibility)"""
    cwd = cwd or "~"
    colors = {
        "uwu": "\033[95m", "feral": "\033[91m", "wizard": "\033[35m",
        "emo": "\033[90m", "rainbow": "\033[33m", "neon": "\033[36m",
        "pastel": "\033[94m", "toxic": "\033[31m"
    }
    symbols = {
        "uwu": "UwU~", "feral": "Rawr", "wizard": "🧙", "emo": "😔",
        "rainbow": "🌈", "neon": "💫", "pastel": "🌸", "toxic": "💀"
    }
    color = colors.get(theme_name, colors["uwu"])
    symbol = symbols.get(theme_name, symbols["uwu"])
    reset = "\033[0m"
    return f"{color}{symbol} [{cwd}]{reset} > "

def display_table(title: str, columns: List[str], data: List[List[Any]]):
    """Display a professional Rich table"""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    for col in columns:
        table.add_column(col)
    for row in data:
        table.add_row(*[str(item) for item in row])
    console.print(table)

def progress_bar(current: int, total: int, width: int = 40, theme: str = "uwu") -> str:
    """Legacy compatibility for progress bar (returns string)"""
    if total == 0: return "[] 0%"
    percentage = current / total
    filled = int(width * percentage)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percentage:.1%}"

def loading_animation(text: str, duration: float = 2.0, theme: str = "uwu"):
    """Show a loading animation for a specified duration"""
    spinner = Spinner(text, theme)
    spinner.start()
    time.sleep(duration)
    spinner.stop()

def typing_effect(text: str, delay: float = 0.05):
    """Simulate typing effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def success_indicator(message: str): console.print(f"[success]✅ {message}[/]")
def error_indicator(message: str): console.print(f"[error]❌ {message}[/]")
def warning_indicator(message: str): console.print(f"[warning]⚠️  {message}[/]")
def info_indicator(message: str): console.print(f"[info]ℹ️  {message}[/]")

# Compatibility
def get_themed_prompt(theme: str, cwd: str = "") -> str: return get_colored_prompt(theme, cwd)
def thunderbolt_effect(): return "⚡⚡⚡"
def bubble_party_effect(): return "🫧🫧"
def psychic_glow_effect(): return "✨🔮✨"
def wizard_hat_effect(): return "🧙"
def emo_tears_effect(): return "💧💧"
def feral_chaos_effect(): return "🔥🔥"
