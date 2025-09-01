# utils/ascii_ui.py
"""
Animated ASCII UI module for UwU-CLI
Provides spinners, themed effects, and visual feedback
"""

import sys
import os
import threading
import time
import random
from typing import Optional

# Global spinner state
spinner_running = False
spinner_thread = None

# Spinner frames for different themes
SPINNER_FRAMES = {
    "default": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
    "uwu": ["UwU", "OwO", "UwU", "OwO", "UwU", "OwO"],
    "feral": ["Rawr", "Grrr", "Rawr", "Grrr", "Rawr", "Grrr"],
    "wizard": ["✨", "🔮", "✨", "🔮", "✨", "🔮"],
    "emo": ["😔", "💔", "😔", "💔", "😔", "💔"]
}

class Spinner:
    """Non-blocking spinner animation"""
    
    def __init__(self, text="Loading", theme="default"):
        self.text = text
        self.theme = theme
        self._running = False
        self._thread = None
        self.frames = SPINNER_FRAMES.get(theme, SPINNER_FRAMES["default"])
        
    def start(self):
        """Start the spinner animation"""
        if self._running:
            return
            
        self._running = True
        def run():
            i = 0
            while self._running:
                frame = self.frames[i % len(self.frames)]
                sys.stdout.write(f"\r{self.text} {frame}")
                sys.stdout.flush()
                i += 1
                time.sleep(0.1)
            # Clear the line when done
            sys.stdout.write("\r" + " " * (len(self.text) + 10) + "\r")
            sys.stdout.flush()
            
        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()
        
    def stop(self):
        """Stop the spinner animation"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.2)

# --- Animated ASCII Effects ---
def thunderbolt_effect() -> str:
    """Return an ASCII thunderbolt for Pokémon roasts"""
    return r"""
        ⚡⚡⚡
      ⚡⚡⚡⚡⚡
        ⚡⚡⚡
    """

def bubble_party_effect() -> str:
    """Return ASCII bubbles for Squirtle-themed roasts"""
    return r"""
     (o)   (o)
    (o o) ( o )
     o   o   o
    """

def psychic_glow_effect() -> str:
    """Return a psychic glow animation placeholder"""
    return r"""
    ~~~~*~~~~*~~~~
    ~*~  ~*~  ~*~
    """

def wizard_hat_effect() -> str:
    """Return a wizard hat effect"""
    return r"""
        /\
       /  \
      /____\
     |      |
     |  ✨  |
     |______|
    """

def emo_tears_effect() -> str:
    """Return emo tears effect"""
    return r"""
     💔  💔
    💧  💧  💧
     😔  😔
    """

def feral_chaos_effect() -> str:
    """Return feral chaos effect"""
    return r"""
    🔥🔥🔥🔥🔥
    💥💥💥💥💥
    🔥🔥🔥🔥🔥
    """

# Theme to effect mapping
THEME_EFFECTS = {
    "uwu": [thunderbolt_effect, bubble_party_effect, psychic_glow_effect],
    "feral": [feral_chaos_effect, thunderbolt_effect],
    "wizard": [wizard_hat_effect, psychic_glow_effect],
    "emo": [emo_tears_effect, bubble_party_effect]
}

def get_random_effect(theme: str) -> Optional[str]:
    """Get a random effect for the given theme"""
    effects = THEME_EFFECTS.get(theme, [])
    if effects:
        return random.choice(effects)()
    return None

def print_with_effect(roast: str, effect: Optional[str] = None, theme: str = "uwu"):
    """
    Print roast with optional ASCII effect
    effect can be 'thunderbolt', 'bubble', 'psychic', 'wizard', 'emo', 'feral', or None
    """
    # If no specific effect given, use theme-appropriate random effect
    if effect is None:
        effect_func = get_random_effect(theme)
        if effect_func:
            print(effect_func)
    elif effect == "thunderbolt":
        print(thunderbolt_effect())
    elif effect == "bubble":
        print(bubble_party_effect())
    elif effect == "psychic":
        print(psychic_glow_effect())
    elif effect == "wizard":
        print(wizard_hat_effect())
    elif effect == "emo":
        print(emo_tears_effect())
    elif effect == "feral":
        print(feral_chaos_effect())
    
    # Print the roast
    print(roast)

# --- Progress Bars ---
def progress_bar(current: int, total: int, width: int = 40, theme: str = "uwu") -> str:
    """Create a themed progress bar"""
    if total == 0:
        return "[] 0%"
        
    percentage = current / total
    filled = int(width * percentage)
    bar = "█" * filled + "░" * (width - filled)
    
    # Theme-specific prefixes
    prefixes = {
        "uwu": "UwU",
        "feral": "Rawr",
        "wizard": "✨",
        "emo": "😔"
    }
    
    prefix = prefixes.get(theme, "→")
    return f"{prefix} [{bar}] {percentage:.1%}"

# --- Loading Animations ---
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

# --- Status Indicators ---
def success_indicator(message: str):
    """Show a success indicator"""
    print(f"✅ {message}")

def error_indicator(message: str):
    """Show an error indicator"""
    print(f"❌ {message}")

def warning_indicator(message: str):
    """Show a warning indicator"""
    print(f"⚠️  {message}")

def info_indicator(message: str):
    """Show an info indicator"""
    print(f"ℹ️  {message}")

# --- Themed Prompts ---
def get_colored_prompt(theme: str, cwd: str = "") -> str:
    """Get a colorful themed prompt string"""
    if not cwd:
        cwd = "~"
    
    # Color codes for Windows and Unix
    if os.name == 'nt':  # Windows
        colors = {
            "uwu": "\033[38;5;213m",      # Pink
            "feral": "\033[38;5;196m",    # Red
            "wizard": "\033[38;5;57m",    # Purple
            "emo": "\033[38;5;240m",      # Gray
            "rainbow": "\033[38;5;208m",  # Orange
            "neon": "\033[38;5;51m",      # Cyan
            "pastel": "\033[38;5;189m",   # Light purple
            "toxic": "\033[38;5;160m"     # Dark red
        }
        reset = "\033[0m"
    else:  # Unix
        colors = {
            "uwu": "\033[95m",      # Magenta
            "feral": "\033[91m",    # Red
            "wizard": "\033[35m",   # Purple
            "emo": "\033[90m",      # Gray
            "rainbow": "\033[33m",  # Yellow
            "neon": "\033[36m",     # Cyan
            "pastel": "\033[94m",   # Blue
            "toxic": "\033[31m"     # Red
        }
        reset = "\033[0m"
    
    # Theme-specific prompts with colors
    prompts = {
        "uwu": f"{colors['uwu']}UwU~ [{cwd}]{reset} > ",
        "feral": f"{colors['feral']}Rawr [{cwd}]{reset} > ",
        "wizard": f"{colors['wizard']}🧙 [{cwd}]{reset} > ",
        "emo": f"{colors['emo']}😔 [{cwd}]{reset} > ",
        "rainbow": f"{colors['rainbow']}🌈 [{cwd}]{reset} > ",
        "neon": f"{colors['neon']}💫 [{cwd}]{reset} > ",
        "pastel": f"{colors['pastel']}🌸 [{cwd}]{reset} > ",
        "toxic": f"{colors['toxic']}💀 [{cwd}]{reset} > "
    }
    
    return prompts.get(theme, f"{colors['uwu']}UwU~ [{cwd}]{reset} > ")

def get_themed_prompt(theme: str, cwd: str = "") -> str:
    """Get a themed prompt string (legacy support)"""
    return get_colored_prompt(theme, cwd)

# --- Example usage ---
if __name__ == "__main__":
    # Test spinner
    test_spinner = Spinner("Testing spinner", "uwu")
    test_spinner.start()
    time.sleep(2)
    test_spinner.stop()
    
    # Test effects
    print_with_effect("Test roast!", effect="thunderbolt")
    print_with_effect("Another test", theme="wizard")
    
    # Test progress bar
    print(progress_bar(75, 100, theme="feral"))
    
    # Test typing effect
    typing_effect("This is a typing effect test...") 