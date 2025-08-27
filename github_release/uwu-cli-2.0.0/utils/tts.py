# utils/tts.py
"""
Text-to-Speech and Export utilities for UwU-CLI
Provides TTS functionality and content export capabilities
"""

import os
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

# Try to import TTS libraries
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# Export directory
EXPORT_DIR = Path.home() / ".uwu-cli" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

# TTS configuration
TTS_CONFIG = {
    "enabled": True,
    "engine": "pyttsx3",  # pyttsx3 or gtts
    "voice": "default",
    "rate": 150,
    "volume": 0.8,
    "language": "en"
}

def load_tts_config() -> Dict[str, Any]:
    """Load TTS configuration from file"""
    config_file = Path.home() / ".uwu-cli" / "tts_config.json"
    
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                TTS_CONFIG.update(config)
        except Exception as e:
            print(f"⚠️  Failed to load TTS config: {e}")
    
    return TTS_CONFIG

def save_tts_config(config: Dict[str, Any]):
    """Save TTS configuration to file"""
    config_file = Path.home() / ".uwu-cli" / "tts_config.json"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"⚠️  Failed to save TTS config: {e}")

def speak(text: str, engine: Optional[str] = None) -> bool:
    """
    Speak text aloud using available TTS engines
    Returns True if successful, False otherwise
    """
    if not TTS_CONFIG.get("enabled", True):
        print("🔇 TTS is disabled")
        return False
    
    engine = engine or TTS_CONFIG.get("engine", "pyttsx3")
    
    if engine == "pyttsx3" and TTS_AVAILABLE:
        return _speak_pyttsx3(text)
    elif engine == "gtts" and GTTS_AVAILABLE:
        return _speak_gtts(text)
    else:
        print("⚠️  No TTS engine available. Install pyttsx3 or gtts")
        return False

def _speak_pyttsx3(text: str) -> bool:
    """Speak using pyttsx3 engine"""
    try:
        engine = pyttsx3.init()
        
        # Configure voice
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        
        # Configure rate and volume
        engine.setProperty('rate', TTS_CONFIG.get("rate", 150))
        engine.setProperty('volume', TTS_CONFIG.get("volume", 0.8))
        
        # Speak the text
        engine.say(text)
        engine.runAndWait()
        
        return True
    except Exception as e:
        print(f"❌ pyttsx3 TTS error: {e}")
        return False

def _speak_gtts(text: str) -> bool:
    """Speak using gTTS engine"""
    try:
        # Create temporary audio file
        temp_file = EXPORT_DIR / f"tts_{int(time.time())}.mp3"
        
        # Generate speech
        tts = gTTS(text=text, lang=TTS_CONFIG.get("language", "en"))
        tts.save(str(temp_file))
        
        # Play the audio (platform-dependent)
        if os.name == 'nt':  # Windows
            os.system(f'start {temp_file}')
        elif os.name == 'posix':  # macOS/Linux
            os.system(f'open {temp_file}' if os.uname().sysname == 'Darwin' else f'xdg-open {temp_file}')
        
        # Clean up after a delay
        def cleanup():
            time.sleep(5)  # Wait for audio to play
            try:
                temp_file.unlink()
            except:
                pass
        
        import threading
        threading.Thread(target=cleanup, daemon=True).start()
        
        return True
    except Exception as e:
        print(f"❌ gTTS error: {e}")
        return False

def export_text(text: str, filename: Optional[str] = None, format: str = "txt") -> str:
    """
    Export text to a file
    Returns the path to the exported file
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"uwu_export_{timestamp}.{format}"
    
    file_path = EXPORT_DIR / filename
    
    try:
        if format.lower() == "json":
            # Export as JSON with metadata
            export_data = {
                "text": text,
                "timestamp": datetime.now().isoformat(),
                "source": "UwU-CLI",
                "version": "2.0.0"
            }
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
        elif format.lower() == "md":
            # Export as Markdown
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# UwU-CLI Export\n\n")
                f.write(f"**Timestamp:** {datetime.now().isoformat()}\n\n")
                f.write(f"**Content:**\n\n{text}\n")
        else:
            # Default: plain text
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"UwU-CLI Export - {datetime.now().isoformat()}\n")
                f.write("=" * 50 + "\n\n")
                f.write(text)
        
        return str(file_path)
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return ""

def export_roast(roast: str, context: str = "", theme: str = "uwu") -> str:
    """Export a roast with context and theme information"""
    export_data = {
        "roast": roast,
        "context": context,
        "theme": theme,
        "timestamp": datetime.now().isoformat(),
        "source": "UwU-CLI",
        "version": "2.0.0"
    }
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"roast_{theme}_{timestamp}.json"
    
    file_path = EXPORT_DIR / filename
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        return str(file_path)
    except Exception as e:
        print(f"❌ Roast export failed: {e}")
        return ""

def export_session_history(history: list, filename: Optional[str] = None) -> str:
    """Export session history to a file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"session_history_{timestamp}.json"
    
    file_path = EXPORT_DIR / filename
    
    try:
        export_data = {
            "session_history": history,
            "export_timestamp": datetime.now().isoformat(),
            "total_commands": len(history),
            "source": "UwU-CLI",
            "version": "2.0.0"
        }
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return str(file_path)
    except Exception as e:
        print(f"❌ Session export failed: {e}")
        return ""

def list_exports() -> list:
    """List all exported files"""
    if not EXPORT_DIR.exists():
        return []
    
    exports = []
    for file_path in EXPORT_DIR.iterdir():
        if file_path.is_file():
            stat = file_path.stat()
            exports.append({
                "filename": file_path.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "path": str(file_path)
            })
    
    return sorted(exports, key=lambda x: x["modified"], reverse=True)

def clear_exports(older_than_days: Optional[int] = None) -> int:
    """Clear exported files, optionally keeping recent ones"""
    if not EXPORT_DIR.exists():
        return 0
    
    cleared_count = 0
    current_time = time.time()
    
    for file_path in EXPORT_DIR.iterdir():
        if file_path.is_file():
            file_age_days = (current_time - file_path.stat().st_mtime) / (24 * 3600)
            
            if older_than_days is None or file_age_days > older_than_days:
                try:
                    file_path.unlink()
                    cleared_count += 1
                except Exception as e:
                    print(f"⚠️  Failed to delete {file_path}: {e}")
    
    return cleared_count

def get_export_summary() -> str:
    """Get a summary of export directory"""
    exports = list_exports()
    total_size = sum(exp["size"] for exp in exports)
    
    summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    UwU-CLI Export Summary                    ║
╚══════════════════════════════════════════════════════════════╝

📁 Export Directory: {EXPORT_DIR}
📊 Total Files: {len(exports)}
💾 Total Size: {total_size / 1024:.1f} KB

🔊 TTS Status: {'Available' if (TTS_AVAILABLE or GTTS_AVAILABLE) else 'Not Available'}
🎵 TTS Engine: {TTS_CONFIG.get('engine', 'None')}
🔇 TTS Enabled: {'Yes' if TTS_CONFIG.get('enabled') else 'No'}

📝 Recent Exports:
"""
    
    for exp in exports[:5]:  # Show last 5 exports
        size_kb = exp["size"] / 1024
        summary += f"  • {exp['filename']} ({size_kb:.1f} KB) - {exp['modified'][:19]}\n"
    
    if len(exports) > 5:
        summary += f"  ... and {len(exports) - 5} more files\n"
    
    return summary

# --- Utility Functions ---
def test_tts() -> str:
    """Test TTS functionality"""
    test_text = "Hello from UwU-CLI! This is a test of the text-to-speech system."
    
    if not TTS_CONFIG.get("enabled", True):
        return "🔇 TTS is disabled in configuration"
    
    if TTS_AVAILABLE:
        result = speak(test_text, "pyttsx3")
        if result:
            return "✅ pyttsx3 TTS test successful"
        else:
            return "❌ pyttsx3 TTS test failed"
    
    if GTTS_AVAILABLE:
        result = speak(test_text, "gtts")
        if result:
            return "✅ gTTS TTS test successful"
        else:
            return "❌ gTTS TTS test failed"
    
    return "❌ No TTS engines available"

def install_tts_dependencies() -> str:
    """Provide instructions for installing TTS dependencies"""
    instructions = """
To enable TTS functionality, install one of these packages:

🔊 pyttsx3 (recommended for offline use):
  pip install pyttsx3

🎵 gTTS (requires internet, better voice quality):
  pip install gTTS

📦 For Windows users, pyttsx3 may require additional setup:
  pip install pywin32

After installation, restart UwU-CLI to enable TTS features.
    """
    return instructions

# --- Configuration Commands ---
def set_tts_engine(engine: str) -> bool:
    """Set the preferred TTS engine"""
    if engine not in ["pyttsx3", "gtts"]:
        print("❌ Invalid engine. Use 'pyttsx3' or 'gtts'")
        return False
    
    if engine == "pyttsx3" and not TTS_AVAILABLE:
        print("❌ pyttsx3 not available. Install with: pip install pyttsx3")
        return False
    
    if engine == "gtts" and not GTTS_AVAILABLE:
        print("❌ gTTS not available. Install with: pip install gtts")
        return False
    
    TTS_CONFIG["engine"] = engine
    save_tts_config(TTS_CONFIG)
    print(f"✅ TTS engine set to: {engine}")
    return True

def set_tts_voice(voice_id: str) -> bool:
    """Set TTS voice (pyttsx3 only)"""
    if not TTS_AVAILABLE:
        print("❌ pyttsx3 not available")
        return False
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        if voice_id.isdigit():
            voice_id = int(voice_id)
            if 0 <= voice_id < len(voices):
                TTS_CONFIG["voice"] = voice_id
                save_tts_config(TTS_CONFIG)
                print(f"✅ Voice set to: {voices[voice_id].name}")
                return True
            else:
                print(f"❌ Invalid voice ID. Available: 0-{len(voices)-1}")
                return False
        else:
            # Try to find voice by name
            for i, voice in enumerate(voices):
                if voice_id.lower() in voice.name.lower():
                    TTS_CONFIG["voice"] = i
                    save_tts_config(TTS_CONFIG)
                    print(f"✅ Voice set to: {voice.name}")
                    return True
            
            print(f"❌ Voice '{voice_id}' not found")
            return False
            
    except Exception as e:
        print(f"❌ Failed to set voice: {e}")
        return False

def list_available_voices() -> list:
    """List available TTS voices"""
    if not TTS_AVAILABLE:
        return []
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        voice_list = []
        for i, voice in enumerate(voices):
            voice_list.append({
                "id": i,
                "name": voice.name,
                "languages": getattr(voice, 'languages', []),
                "gender": getattr(voice, 'gender', 'unknown')
            })
        
        return voice_list
    except Exception as e:
        print(f"❌ Failed to list voices: {e}")
        return [] 