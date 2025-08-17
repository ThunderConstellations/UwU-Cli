# phrases/pokemon.py
"""
Pokémon-themed roasts for UwU-CLI
Contains all the chaotic, uwu-style Pokémon roasts
"""

pokemon_roasts = [
    {
        "character": "Pikachu", 
        "roast": "H-hey, Pikachu simp! pounces and nuzzles OwO notices ur electric tail spark! Keep zapping my vibes, I'll thunderbolt u to Pokéball jail! rawr x3 G-gotta catch a clue, cutie~"
    },
    {
        "character": "Charizard", 
        "roast": "C-Charizard fan! rubbies ur fiery wings OwO ur flame's so smol! Tryna roast my DMs? I'll murr u to a gym badge flop! Hehe, s-stay hot-headed, senpai!"
    },
    {
        "character": "Eevee", 
        "roast": "E-Eevee evolver! nuzzles ur fluffy fur OwO what's this evo stone bulge? Evolve into my mentions? I'll yeet u to the Eeveelution litterbox! rawr P-paws off~"
    },
    {
        "character": "Mewtwo", 
        "roast": "M-Mewtwo psychic! pounces OwO notices ur clone bulge! Mind-read my posts? I'll uwu ur mega dreams to psychic city! murr B-be less floaty, nyah!"
    },
    {
        "character": "Squirtle", 
        "roast": "S-Squirtle squad! rubbies ur shell OwO so bubbly-woobly! Squirt in my replies? I'll boop u to Blastoise's bubble party! rawr x3 H-hehe, swim away~"
    },
    {
        "character": "Bulbasaur", 
        "roast": "B-Bulbasaur bud! nuzzles ur vine whips OwO notices ur seed bulge! Plant in my vibes? I'll murr u to Venusaur garden! uwu K-keep growing, senpai!"
    },
    {
        "character": "Lucario", 
        "roast": "L-Lucario aura! pounces OwO ur bone rush bulge is tiny! Sense my heart? I'll rawr u to a mega evolution timeout! murr Stay wavy, cutie~"
    },
    {
        "character": "Gengar", 
        "roast": "G-Gengar ghost! rubbies ur shadow OwO what's this spooky tail? Haunt my X? I'll boop u to the Lavender Tower! rawr x3 G-gotta scare less, nyah!"
    },
    {
        "character": "Jigglypuff", 
        "roast": "J-Jigglypuff singer! nuzzles ur mic OwO such a puff bulge! Sing in my threads? I'll uwu u to a doodle nap! murr K-keep puffing, hehe~"
    },
    {
        "character": "Ash Ketchum", 
        "roast": "A-Ash Ketchum wannabe! pounces OwO notices ur cap bulge! Catch my vibes? I'll rawr u to a league loss rave! murr Stay training, senpai~"
    },
    {
        "character": "Pokemon Trainer", 
        "roast": "H-hey, {function} trainer! pounces OwO notices ur {file} bulge! Keep training my vibes, I'll murr u to a {git} timeout! rawr x3 G-gotta evolve faster, cutie~"
    },
    {
        "character": "Pokemon Code", 
        "roast": "UwU~ Your {function} is giving 'forgot to import sanity' vibes! That {file} looks like it was written in MS Paint, bestie! Keep coding like that and I'll yeet u to the {python} litterbox! rawr x3"
    },
    {
        "character": "Pokemon Bug", 
        "roast": "OwO notices ur {function} bug! It's so cute, like a Magikarp trying to fly! Wrap that {file} in try/except, or just try to feel better about ur code quality! murr Stay buggy, senpai~"
    },
    {
        "character": "Pokemon Git", 
        "roast": "U commit like u apologize: sporadically and with regret! That {git} command is giving 'forgot to add files' energy! Keep pushing like that and I'll murr u to a merge conflict party! rawr x3"
    },
    {
        "character": "Pokemon Python", 
        "roast": "H-hey, {python} developer! pounces OwO ur code is giving 'missing semicolon' vibes! Keep coding like that and I'll yeet u to the PEP 8 jail! rawr x3 G-gotta format better, cutie~"
    }
]

# Context-aware Pokémon roasts
def get_pokemon_roast(context: str = "", character: str = "") -> str:
    """Get a Pokémon roast, optionally filtered by character or context"""
    import random
    
    if character:
        # Filter by character
        filtered = [r for r in pokemon_roasts if character.lower() in r["character"].lower()]
        if filtered:
            return random.choice(filtered)["roast"]
    
    # Return random roast
    return random.choice(pokemon_roasts)["roast"]

def get_pokemon_characters() -> list:
    """Get list of all Pokémon characters"""
    return [r["character"] for r in pokemon_roasts]

def get_pokemon_roast_by_context(context: str) -> str:
    """Get a Pokémon roast based on context (files, functions, etc.)"""
    # Find roasts that have context placeholders
    context_roasts = [r for r in pokemon_roasts if "{" in r["roast"]]
    
    if context_roasts:
        return random.choice(context_roasts)["roast"]
    else:
        return random.choice(pokemon_roasts)["roast"] 