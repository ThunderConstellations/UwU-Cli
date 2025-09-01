"""
AI Provider Module for UwU-CLI
Supports multiple AI providers including OpenRouter for flexible model selection
"""

import os
import json
import requests
from typing import Dict, Any, Optional, List
from pathlib import Path

class AIProvider:
    """Base class for AI providers"""
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load AI provider configuration"""
        config_paths = [
            Path.cwd() / "config" / "ai_provider.json",
            Path.home() / ".uwu-cli" / "ai_provider.json",
            Path(os.getenv("APPDATA", Path.home())) / "uwu-cli" / "ai_provider.json"
        ]
        
        for path in config_paths:
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception:
                    continue
        
        # Default configuration
        return {
            "provider": "openrouter",
            "openrouter": {
                "api_key": os.getenv("OPENROUTER_API_KEY", ""),
                "model": os.getenv("UWU_MODEL", "openai/gpt-4o"),
                "base_url": "https://openrouter.ai/api/v1",
                "http_referer": "https://github.com/UwU-CLI/UwU-Cli",
                "x_title": "UwU-CLI"
            }
        }
    
    def get_available_models(self) -> List[str]:
        """Get list of available AI models"""
        return [
            "openai/gpt-4o",
            "openai/gpt-4o-mini", 
            "anthropic/claude-3.5-sonnet",
            "anthropic/claude-3-haiku",
            "deepseek/deepseek-coder",
            "meta-llama/llama-3.1-8b-instruct",
            "google/gemini-pro"
        ]
    
    def chat(self, message: str, model: Optional[str] = None) -> str:
        """Send a chat message to the AI provider"""
        provider = self.config.get("provider", "openrouter")
        
        if provider == "openrouter":
            return self._openrouter_chat(message, model)
        else:
            return f"❌ Unsupported AI provider: {provider}"
    
    def _openrouter_chat(self, message: str, model: Optional[str] = None) -> str:
        """Send chat message to OpenRouter"""
        config = self.config.get("openrouter", {})
        api_key = config.get("api_key")
        
        if not api_key:
            return "❌ OpenRouter API key not configured. Set OPENROUTER_API_KEY environment variable or configure in config/ai_provider.json"
        
        model = model or config.get("model", "openai/gpt-4o")
        base_url = config.get("base_url", "https://openrouter.ai/api/v1")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": config.get("http_referer", "https://github.com/UwU-CLI/UwU-Cli"),
            "X-Title": config.get("x_title", "UwU-CLI")
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"❌ OpenRouter API error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"❌ Error communicating with OpenRouter: {str(e)}"
    
    def set_model(self, model: str) -> str:
        """Set the default AI model"""
        if model not in self.get_available_models():
            return f"❌ Invalid model: {model}. Use /models to see available options."
        
        self.config["openrouter"]["model"] = model
        return f"✅ Default model set to: {model}"
    
    def get_current_model(self) -> str:
        """Get the current default model"""
        return self.config["openrouter"]["model"]

# Global instance
_ai_provider = None

def get_ai_provider() -> AIProvider:
    """Get the global AI provider instance"""
    global _ai_provider
    if _ai_provider is None:
        _ai_provider = AIProvider()
    return _ai_provider 