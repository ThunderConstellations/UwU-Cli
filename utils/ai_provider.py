"""
Unified AI Provider Module for UwU-CLI
Supports multiple AI providers including OpenRouter, background job processing, and local fallback.
"""

import os
import json
import threading
import queue
import requests
import time
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path

# Job Queue for background processing
_job_queue = queue.Queue()
_job_results = {}
_job_counter = 0
_lock = threading.Lock()

class AIProvider:
    """Unified controller for AI operations"""
    
    def __init__(self):
        self.config = self._load_config()
        self._start_worker()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load AI configuration with multi-location discovery and fallbacks"""
        # Default configuration
        config = {
            "provider": "openrouter",
            "openrouter": {
                "api_key": os.getenv("OPENROUTER_API_KEY", ""),
                "model": os.getenv("UWU_MODEL", "openai/gpt-4o"),
                "base_url": "https://openrouter.ai/api/v1",
                "http_referer": "https://github.com/UwU-CLI/UwU-Cli",
                "x_title": "UwU-CLI",
                "timeout_seconds": 30,
                "max_tokens": 1000,
                "temperature": 0.7
            },
            "local": {
                "enabled": False,
                "command_template": ""
            }
        }

        config_paths = [
            Path.cwd() / "config" / "ai_provider.json",
            Path.home() / ".uwu-cli" / "ai_config.json",
            Path.home() / ".uwu-cli" / "ai_provider.json"
        ]
        
        for path in config_paths:
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        file_config = json.load(f)
                        # Deep merge or specific update
                        if "openrouter" in file_config:
                            config["openrouter"].update(file_config["openrouter"])
                        if "provider" in file_config:
                            config["provider"] = file_config["provider"]
                        if "openrouter_api_key" in file_config: # Legacy support for ai.py format
                             config["openrouter"]["api_key"] = file_config["openrouter_api_key"]
                except Exception:
                    continue
        
        return config

    def get_available_models(self) -> List[str]:
        """Get list of common AI models"""
        return [
            "openai/gpt-4o",
            "openai/gpt-4o-mini", 
            "anthropic/claude-3.5-sonnet",
            "deepseek/deepseek-coder",
            "deepseek/deepseek-r1-distill-llama-70b:free",
            "google/gemini-pro"
        ]

    def chat(self, message: str, model: Optional[str] = None, system: Optional[str] = None) -> str:
        """Synchronous chat call"""
        provider = self.config.get("provider", "openrouter")
        
        if self.config.get("local", {}).get("enabled", False):
            return self._local_chat(message)

        if provider == "openrouter":
            return self._openrouter_chat(message, model, system)
        else:
            return f"❌ Unsupported AI provider: {provider}"

    def _openrouter_chat(self, message: str, model: Optional[str] = None, system: Optional[str] = None) -> str:
        """Call OpenRouter API"""
        config = self.config.get("openrouter", {})
        api_key = config.get("api_key")
        
        if not api_key:
            return "❌ OpenRouter API key not configured. Set OPENROUTER_API_KEY environment variable."
        
        model = model or config.get("model", "openai/gpt-4o")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": config.get("http_referer"),
            "X-Title": config.get("x_title")
        }
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": message})

        data = {
            "model": model,
            "messages": messages,
            "max_tokens": config.get("max_tokens", 1000),
            "temperature": config.get("temperature", 0.7)
        }
        
        try:
            response = requests.post(
                f"{config.get('base_url')}/chat/completions",
                headers=headers,
                json=data,
                timeout=config.get("timeout_seconds", 30)
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"❌ AI Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"❌ AI Connection Error: {str(e)}"

    def _local_chat(self, message: str) -> str:
        """Call local LLM via command execution"""
        tmpl = self.config.get("local", {}).get("command_template", "")
        if not tmpl:
            return "❌ Local LLM command template not configured."

        cmd = tmpl.replace("{prompt}", message)
        try:
            import subprocess
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            return result.stdout.strip() if result.returncode == 0 else f"❌ Local AI Error: {result.stderr}"
        except Exception as e:
            return f"❌ Local AI Execution Error: {str(e)}"

    # --- Background Job Management ---

    def submit_job(self, prompt: str, model: Optional[str] = None, system: Optional[str] = None) -> int:
        """Submit a job for background processing"""
        global _job_counter
        with _lock:
            job_id = _job_counter
            _job_counter += 1
            _job_queue.put((job_id, prompt, model, system))
        return job_id

    def get_job_result(self, job_id: int) -> Optional[str]:
        """Retrieve the result of a job"""
        return _job_results.get(job_id)

    def _start_worker(self):
        """Start the background worker thread"""
        worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        worker_thread.start()

    def _worker_loop(self):
        """Process jobs from the queue"""
        while True:
            try:
                job_id, prompt, model, system = _job_queue.get()
                result = self.chat(prompt, model, system)
                _job_results[job_id] = result
                _job_queue.task_done()
            except Exception:
                time.sleep(1)

# Global singleton
_instance = None

def get_ai_provider() -> AIProvider:
    """Get or create the global AIProvider instance"""
    global _instance
    if _instance is None:
        _instance = AIProvider()
    return _instance

# Compatibility functions for existing code using utils.ai patterns
def submit_ai_job(prompt: str, mode: str = "openrouter") -> int:
    return get_ai_provider().submit_job(prompt)

def get_job_result(job_id: int) -> Optional[str]:
    return get_ai_provider().get_job_result(job_id)

def load_config() -> Dict[str, Any]:
    return get_ai_provider().config
