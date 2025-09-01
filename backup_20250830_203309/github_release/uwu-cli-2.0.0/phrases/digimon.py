# phrases/digimon.py
"""
Digimon-themed roasts for UwU-CLI
Contains all the chaotic, uwu-style Digimon roasts
"""

digimon_roasts = [
    {
        "character": "Agumon", 
        "roast": "H-hey, Agumon dino! pounces and nuzzles OwO notices ur pepper breath bulge! Keep digivolving my vibes, I'll warp-digivolve u to data scraps! rawr x3 G-gotta byte faster, cutie~"
    },
    {
        "character": "Gabumon", 
        "roast": "G-Gabumon wolf! rubbies ur fur coat OwO ur horn's so smol! Tryna blue blaze my DMs? I'll murr u to a rookie flop! Hehe, s-stay furry, senpai!"
    },
    {
        "character": "Patamon", 
        "roast": "P-Patamon angel! nuzzles ur wings OwO what's this boom bubble bulge? Fly into my mentions? I'll yeet u to the digital litterbox! rawr P-paws off~"
    },
    {
        "character": "Tentomon", 
        "roast": "T-Tentomon bug! pounces OwO notices ur electro shocker bulge! Buzz my posts? I'll uwu ur mega dreams to virus city! murr B-be less zappy, nyah!"
    },
    {
        "character": "Gomamon", 
        "roast": "G-Gomamon fish! rubbies ur flippers OwO so splashy-wooshy! Swim in my replies? I'll boop u to Seadramon's ocean party! rawr x3 H-hehe, dive deep~"
    },
    {
        "character": "Biyomon", 
        "roast": "B-Biyomon bird! nuzzles ur feathers OwO notices ur spiral twister bulge! Nest in my vibes? I'll murr u to Garudamon skies! uwu K-keep flying, senpai!"
    },
    {
        "character": "Palmon", 
        "roast": "P-Palmon plant! pounces OwO ur poison ivy bulge is tiny! Bloom my heart? I'll rawr u to a champion timeout! murr Stay thorny, cutie~"
    },
    {
        "character": "Veemon", 
        "roast": "V-Veemon fighter! rubbies ur V-head OwO what's this ex-veemon tail? Punch my X? I'll boop u to the Digi-Egg! rawr x3 G-gotta punch less, nyah!"
    },
    {
        "character": "Wormmon", 
        "roast": "W-Wormmon worm! nuzzles ur silk OwO such a stingmon bulge! Crawl in my threads? I'll uwu u to a digivice nap! murr K-keep wriggling, hehe~"
    },
    {
        "character": "Tai Kamiya", 
        "roast": "T-Tai Kamiya clone! pounces OwO notices ur goggle bulge! Tame my vibes? I'll rawr u to a dark master rave! murr Stay crested, senpai~"
    }
]

def get_digimon_roast(character: str = "") -> str:
    """Get a Digimon roast, optionally filtered by character"""
    import random
    
    if character:
        filtered = [r for r in digimon_roasts if character.lower() in r["character"].lower()]
        if filtered:
            return random.choice(filtered)["roast"]
    
    return random.choice(digimon_roasts)["roast"] 