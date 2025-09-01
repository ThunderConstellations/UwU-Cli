# utils/config.py
"""
Configuration management for UwU-CLI
Handles user preferences, aliases, and settings
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Configuration file paths
CONFIG_DIR = Path.home() / ".uwu-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"
ALIAS_FILE = CONFIG_DIR / "aliases.json"

# Default configuration
DEFAULT_CONFIG = {
    "prompt_style": "uwu",
    "enable_telemetry": False,
    "phrase_pack": "default",
    "auto_save_every": 10,
    "max_history": 500,
    "safe_mode": False,
    "theme_colors": True,
    "ascii_effects": True,
    "sound_enabled": False,
    "plugins_enabled": True,
    "ai_enabled": True,
    "default_ai_model": "gpt-4o-mini"
}

# Default aliases
DEFAULT_ALIASES = {
    "ll": "ls -la",
    "gs": "git status",
    "gp": "git push",
    "gc": "git commit -m",
    "ga": "git add",
    "gl": "git log --oneline",
    "gb": "git branch",
    "gco": "git checkout",
    "gcb": "git checkout -b",
    "uwu": "uwu_cli.py",
    "uwu-cli": "uwu_cli.py",
    "uwuhelp": "help",
    "uwutheme": "theme",
    "uwuconfig": "config",
    "uwualias": "alias"
}

def ensure_config_dir():
    """Ensure configuration directory exists"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config() -> Dict[str, Any]:
    """Load configuration from file"""
    ensure_config_dir()
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged_config = DEFAULT_CONFIG.copy()
                merged_config.update(config)
                return merged_config
        except Exception as e:
            print(f"⚠️  Failed to load config: {e}")
            return DEFAULT_CONFIG.copy()
    else:
        # Create default config file
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]):
    """Save configuration to file"""
    ensure_config_dir()
    
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️  Failed to save config: {e}")

def get_config_value(key: str, default: Any = None) -> Any:
    """Get a specific configuration value"""
    config = load_config()
    return config.get(key, default)

def set_config_value(key: str, value: Any):
    """Set a specific configuration value"""
    config = load_config()
    config[key] = value
    save_config(config)

def load_aliases() -> Dict[str, str]:
    """Load aliases from file"""
    ensure_config_dir()
    
    if ALIAS_FILE.exists():
        try:
            with open(ALIAS_FILE, "r", encoding="utf-8") as f:
                aliases = json.load(f)
                # Merge with defaults
                merged_aliases = DEFAULT_ALIASES.copy()
                merged_aliases.update(aliases)
                return merged_aliases
        except Exception as e:
            print(f"⚠️  Failed to load aliases: {e}")
            return DEFAULT_ALIASES.copy()
    else:
        # Create default aliases file
        save_aliases(DEFAULT_ALIASES)
        return DEFAULT_ALIASES.copy()

def save_aliases(aliases: Dict[str, str]):
    """Save aliases to file"""
    ensure_config_dir()
    
    try:
        with open(ALIAS_FILE, "w", encoding="utf-8") as f:
            json.dump(aliases, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️  Failed to save aliases: {e}")

def get_alias(alias_name: str) -> Optional[str]:
    """Get an alias value"""
    aliases = load_aliases()
    return aliases.get(alias_name)

def set_alias(alias_name: str, command: str):
    """Set an alias"""
    aliases = load_aliases()
    aliases[alias_name] = command
    save_aliases(aliases)

def remove_alias(alias_name: str) -> bool:
    """Remove an alias"""
    aliases = load_aliases()
    if alias_name in aliases:
        del aliases[alias_name]
        save_aliases(aliases)
        return True
    return False

def list_aliases() -> Dict[str, str]:
    """List all aliases"""
    return load_aliases()

def clear_aliases():
    """Clear all custom aliases (restore defaults)"""
    save_aliases(DEFAULT_ALIASES)

def export_config() -> str:
    """Export current configuration as JSON string"""
    config = load_config()
    aliases = load_aliases()
    
    export_data = {
        "config": config,
        "aliases": aliases,
        "export_timestamp": str(Path().cwd()),
        "uwu_cli_version": "2.0.0"
    }
    
    return json.dumps(export_data, indent=2, ensure_ascii=False)

def import_config(config_json: str) -> bool:
    """Import configuration from JSON string"""
    try:
        data = json.loads(config_json)
        
        if "config" in data:
            save_config(data["config"])
        
        if "aliases" in data:
            save_aliases(data["aliases"])
            
        return True
    except Exception as e:
        print(f"⚠️  Failed to import config: {e}")
        return False

def reset_config():
    """Reset configuration to defaults"""
    save_config(DEFAULT_CONFIG)
    save_aliases(DEFAULT_ALIASES)

def validate_config(config: Dict[str, Any]) -> Dict[str, str]:
    """Validate configuration and return any errors"""
    errors = {}
    
    # Validate prompt_style
    valid_styles = ["uwu", "feral", "wizard", "emo"]
    if config.get("prompt_style") not in valid_styles:
        errors["prompt_style"] = f"Must be one of: {', '.join(valid_styles)}"
    
    # Validate numeric values
    if config.get("auto_save_every", 0) < 1:
        errors["auto_save_every"] = "Must be at least 1"
    
    if config.get("max_history", 0) < 10:
        errors["max_history"] = "Must be at least 10"
    
    # Validate boolean values
    boolean_keys = ["enable_telemetry", "safe_mode", "theme_colors", "ascii_effects", "sound_enabled", "plugins_enabled", "ai_enabled"]
    for key in boolean_keys:
        if key in config and not isinstance(config[key], bool):
            errors[key] = "Must be true or false"
    
    return errors

def get_config_summary() -> str:
    """Get a human-readable summary of current configuration"""
    config = load_config()
    aliases = load_aliases()
    
    summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    UwU-CLI Configuration                     ║
╚══════════════════════════════════════════════════════════════╝

🎨 Theme: {config.get('prompt_style', 'uwu')}
📊 Telemetry: {'Enabled' if config.get('enable_telemetry') else 'Disabled'}
🔒 Safe Mode: {'Enabled' if config.get('safe_mode') else 'Disabled'}
🎭 ASCII Effects: {'Enabled' if config.get('ascii_effects') else 'Disabled'}
🔊 Sound: {'Enabled' if config.get('sound_enabled') else 'Disabled'}
🔌 Plugins: {'Enabled' if config.get('plugins_enabled') else 'Disabled'}
🤖 AI: {'Enabled' if config.get('ai_enabled') else 'Disabled'}
📝 History: {config.get('max_history', 500)} commands
💾 Auto-save: Every {config.get('auto_save_every', 10)} commands

🔗 Aliases: {len(aliases)} configured
📁 Config Location: {CONFIG_FILE}
    """
    
    return summary

# --- Environment Variable Support ---
def load_env_config():
    """Load configuration from environment variables"""
    config = load_config()
    
    # Check for environment variable overrides
    env_mappings = {
        "UWU_CLI_THEME": "prompt_style",
        "UWU_CLI_TELEMETRY": "enable_telemetry",
        "UWU_CLI_SAFE_MODE": "safe_mode",
        "UWU_CLI_ASCII_EFFECTS": "ascii_effects",
        "UWU_CLI_SOUND": "sound_enabled",
        "UWU_CLI_PLUGINS": "plugins_enabled",
        "UWU_CLI_AI": "ai_enabled"
    }
    
    for env_var, config_key in env_mappings.items():
        env_value = os.environ.get(env_var)
        if env_value is not None:
            if config_key in ["enable_telemetry", "safe_mode", "theme_colors", "ascii_effects", "sound_enabled", "plugins_enabled", "ai_enabled"]:
                # Convert string to boolean
                config[config_key] = env_value.lower() in ["true", "1", "yes", "on"]
            else:
                config[config_key] = env_value
    
    return config

# --- Configuration Profiles ---
def create_profile(profile_name: str, config: Dict[str, Any]):
    """Create a named configuration profile"""
    ensure_config_dir()
    profile_file = CONFIG_DIR / f"profile_{profile_name}.json"
    
    try:
        with open(profile_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"⚠️  Failed to create profile: {e}")
        return False

def load_profile(profile_name: str) -> Optional[Dict[str, Any]]:
    """Load a named configuration profile"""
    profile_file = CONFIG_DIR / f"profile_{profile_name}.json"
    
    if profile_file.exists():
        try:
            with open(profile_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Failed to load profile: {e}")
            return None
    return None

def list_profiles() -> list:
    """List all available configuration profiles"""
    ensure_config_dir()
    profiles = []
    
    for profile_file in CONFIG_DIR.glob("profile_*.json"):
        profile_name = profile_file.stem.replace("profile_", "")
        profiles.append(profile_name)
    
    return profiles

def delete_profile(profile_name: str) -> bool:
    """Delete a named configuration profile"""
    profile_file = CONFIG_DIR / f"profile_{profile_name}.json"
    
    if profile_file.exists():
        try:
            profile_file.unlink()
            return True
        except Exception as e:
            print(f"⚠️  Failed to delete profile: {e}")
            return False
    return False 