"""
AI integration proxy for UwU-CLI
Proxies requests to the unified AIProvider in ai_provider.py
"""
from utils.ai_provider import get_ai_provider, submit_ai_job, get_job_result, load_config

def save_config(config):
    import json
    from pathlib import Path
    config_file = Path.home() / ".uwu-cli" / "ai_config.json"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

def generate_roast_variants(text, config):
    prompt = f"Generate 3 style variants (UWU, FERAL, WIZARD) for: {text}"
    return submit_ai_job(prompt)

def parse_roast_variants(ai_response):
    variants = {}
    lines = ai_response.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('UWU:'): variants['uwu'] = line[4:].strip()
        elif line.startswith('FERAL:'): variants['feral'] = line[6:].strip()
        elif line.startswith('WIZARD:'): variants['wizard'] = line[8:].strip()
    return variants
