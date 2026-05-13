import requests
import os
import json
from typing import Dict, Any, Optional

def call_openrouter(prompt: str, config: Dict[str, Any], system: Optional[str] = None) -> str:
    """Call OpenRouter API to get response"""
    api_key = config.get("api_key") or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "[ERROR] OpenRouter API key not configured."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": config.get("model", "openai/gpt-4o"),
        "messages": [
            {"role": "system", "content": system or "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"[ERROR] API returned {response.status_code}: {response.text}"
    except Exception as e:
        return f"[ERROR] Request failed: {str(e)}"

def submit_ai_job(prompt: str, provider: str = "openrouter"):
    # Mocking for this specific task context if necessary
    # In a real app this would queue a job.
    # For now, let's keep it simple.
    from utils.config import load_config
    config = load_config().get("ai_provider", {})
    return call_openrouter(prompt, config)

def get_job_result(job_id: int):
    return "Job complete (mocked result)"

def load_config():
    # Placeholder
    return {}
