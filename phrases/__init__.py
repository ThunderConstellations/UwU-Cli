"""
Phrases module for UwU-CLI
Imports all phrase modules and provides unified access
"""

try: from .pokemon import pokemon_roasts
except ImportError: pokemon_roasts = []

try: from .digimon import digimon_roasts
except ImportError: digimon_roasts = []

try: from .mtg import mtg_roasts
except ImportError: mtg_roasts = []

try: from .yugioh import yugioh_roasts
except ImportError: yugioh_roasts = []

try: from .cringey import cringey_roasts
except ImportError: cringey_roasts = []

try: from .toxic import toxic_roasts
except ImportError: toxic_roasts = []

try: from .facts import cringey_facts
except ImportError: cringey_facts = []

# Aggregate all phrase roasts
ALL_PHRASES = {
    "pokemon": pokemon_roasts,
    "digimon": digimon_roasts,
    "mtg": mtg_roasts,
    "yugioh": yugioh_roasts,
    "cringey": cringey_roasts,
    "toxic": toxic_roasts,
    "facts": cringey_facts
}

def get_random_phrase(theme=None):
    import random
    if theme and theme in ALL_PHRASES and ALL_PHRASES[theme]:
        return random.choice(ALL_PHRASES[theme])["roast"]

    available = [t for t, p in ALL_PHRASES.items() if p]
    if not available: return "UwU system failure!"
    theme_choice = random.choice(available)
    return random.choice(ALL_PHRASES[theme_choice])["roast"]

def get_total_phrase_count():
    return sum(len(phrases) for phrases in ALL_PHRASES.values())
