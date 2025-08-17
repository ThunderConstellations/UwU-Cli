# phrases/__init__.py
"""
Phrases module for UwU-CLI
Imports all phrase modules and provides unified access
"""

try:
    from .pokemon import pokemon_roasts
except ImportError:
    pokemon_roasts = []

try:
    from .digimon import digimon_roasts
except ImportError:
    digimon_roasts = []

try:
    from .mtg import mtg_roasts
except ImportError:
    mtg_roasts = []

try:
    from .yugioh import yugioh_roasts
except ImportError:
    yugioh_roasts = []

try:
    from .cringey import cringey_roasts
except ImportError:
    cringey_roasts = []

# Aggregate all phrase roasts
ALL_PHRASES = {
    "pokemon": pokemon_roasts,
    "digimon": digimon_roasts,
    "mtg": mtg_roasts,
    "yugioh": yugioh_roasts,
    "cringey": cringey_roasts
}

def get_random_phrase(theme=None):
    """Get a random phrase, optionally filtered by theme"""
    import random
    
    if theme and theme in ALL_PHRASES:
        return random.choice(ALL_PHRASES[theme])["roast"]
    
    # Random across all themes
    theme_choice = random.choice(list(ALL_PHRASES.keys()))
    return random.choice(ALL_PHRASES[theme_choice])["roast"]

def get_phrase_by_theme(theme):
    """Get all phrases for a specific theme"""
    return ALL_PHRASES.get(theme, [])

def get_available_themes():
    """Get list of available phrase themes"""
    return list(ALL_PHRASES.keys())

def get_total_phrase_count():
    """Get total number of phrases across all themes"""
    return sum(len(phrases) for phrases in ALL_PHRASES.values()) 