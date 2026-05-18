"""
Animated Chaotic ASCII UI module for UwU-CLI using Rich
Provides sparkly spinners, cringe effects, and chaotic visual feedback.
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
from rich.live import Live

# Initialize Rich Console with a chaotic theme
custom_theme = Theme({
    "uwu": "bold magenta",
    "feral": "bold reverse red",
    "wizard": "italic cyan",
    "emo": "dim white on black",
    "rainbow": "bold yellow",
    "neon": "bold bright_cyan",
    "pastel": "bright_magenta",
    "toxic": "bold bright_green on black",
    "info": "blue",
    "warning": "blink yellow",
    "error": "bold red",
    "success": "green"
})

console = Console(theme=custom_theme)

# Cringe sparkly frames
SPARKLES = ["✨", "🌟", "💫", "⭐", "🌈", "💖"]

class Spinner:
    """Chaotic sparkly spinner"""
    def __init__(self, text="Processing...", theme="uwu"):
        self.text = f"{random.choice(SPARKLES)} {text} {random.choice(SPARKLES)}"
        self._progress = Progress(
            SpinnerColumn(spinner_name="dots12"),
            TextColumn("[bold magenta]{task.description}[/]"),
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
    """Print text inside a chaotic sparkly panel"""
    style = theme if theme in custom_theme.styles else "uwu"

    # Randomly add "cringe" decorators to the title
    decorators = ["x3", "nyah~", "bestie", "OwO", "UwU", "rawr"]
    title = f"{random.choice(SPARKLES)} UwU [{theme}] {random.choice(decorators)} {random.choice(SPARKLES)}"

    # Re-implement legacy effects as Rich components
    if effect == "thunderbolt":
        console.print("[bold yellow]⚡⚡⚡ ZAP! ⚡⚡⚡[/]")
    elif effect == "bubble":
        console.print("[blue]🫧 🫧 Pop! 🫧 🫧[/]")
    elif effect == "psychic":
        console.print("[magenta]🔮 ✨ Sensing vibes... ✨ 🔮[/]")
    elif effect == "wizard":
        console.print("[cyan]🧙‍♂️ ✨ CASTING SPELL... ✨[/]")
    elif effect == "emo":
        console.print("[dim]💧 💔 Life is pain 💔 💧[/]")
    elif effect == "feral":
        console.print("[bold red]🔥🔥🔥 CHAOS!!! 🔥🔥🔥[/]")

    console.print(Panel(text, title=title, border_style=style, padding=(1, 2)))

def get_colored_prompt(theme_name: str, cwd: str = "") -> str:
    """Get a chaotic colorful themed prompt"""
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
    """Display a professional but sparkly Rich table"""
    table = Table(title=f"✨ {title} ✨", show_header=True, header_style="bold magenta", border_style="cyan")
    for col in columns:
        table.add_column(col)
    for row in data:
        table.add_row(*[str(item) for item in row])
    console.print(table)

def success_indicator(message: str): console.print(f"[success]✨ ✅ {message} ✨[/]")
def error_indicator(message: str): console.print(f"[error]💀 ❌ {message} 💀[/]")
def warning_indicator(message: str): console.print(f"[warning]⚠️  {message} ⚠️[/]")
def info_indicator(message: str): console.print(f"[info]🌸 ℹ️  {message} 🌸[/]")

# Legacy compatibility
def get_themed_prompt(theme: str, cwd: str = "") -> str: return get_colored_prompt(theme, cwd)
def thunderbolt_effect(): return "⚡⚡⚡"
def bubble_party_effect(): return "🫧🫧"
def psychic_glow_effect(): return "✨🔮✨"
def wizard_hat_effect(): return "🧙"
def emo_tears_effect(): return "💧💧"
def feral_chaos_effect(): return "🔥🔥"
