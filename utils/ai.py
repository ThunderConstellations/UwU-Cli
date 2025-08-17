# utils/ai.py
"""
AI integration module for UwU-CLI
Handles OpenRouter API calls, local LLM fallback, and background job processing
"""

import threading
import queue
import time
import json
import os
from typing import Optional, Dict, Any, List
from pathlib import Path

# Try to import requests for OpenRouter API calls
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  requests module not available. OpenRouter features will be disabled.")

# Job Queue
job_queue = queue.Queue()
job_results = {}
job_counter = 0
lock = threading.Lock()

# Default configuration
DEFAULT_CONFIG = {
    "openrouter_api_key": "",
    "use_local_llm": False,
    "local_llm_cmd": "",
    "model": "deepseek/deepseek-r1-0528:free",
    "timeout_seconds": 30,
    "max_tokens": 1000,
    "temperature": 0.9
}


def load_config() -> Dict[str, Any]:
    """Load AI configuration from file or environment variables"""
    config = DEFAULT_CONFIG.copy()

    # Check for config file
    config_file = Path.home() / ".uwu-cli" / "ai_config.json"
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            print(f"⚠️  Failed to load AI config: {e}")

    # Check environment variables
    env_key = os.environ.get("OPENROUTER_API_KEY")
    if env_key:
        config["openrouter_api_key"] = env_key

    return config


def save_config(config: Dict[str, Any]):
    """Save AI configuration to file"""
    config_file = Path.home() / ".uwu-cli" / "ai_config.json"
    config_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"⚠️  Failed to save AI config: {e}")


def call_openrouter(prompt: str, config: Dict[str, Any], system: Optional[str] = None) -> str:
    """Call OpenRouter API to get response"""
    if not REQUESTS_AVAILABLE:
        return "[ERROR] requests module not available. Install with: pip install requests"

    api_key = config.get("openrouter_api_key")
    if not api_key:
        return "[ERROR] OpenRouter API key not configured. Set OPENROUTER_API_KEY environment variable or configure in ~/.uwu-cli/ai_config.json"

    url = "https://api.openrouter.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/ThunderConstellations/UwU-Cli",
        "X-Title": "UwU-CLI"
    }

    # Default toxic system prompt if none provided
    if not system:
        system = """You are a chaotic, toxic AI assistant with UwU energy. Be savage, witty, and absolutely ruthless in your responses. Use internet slang, gaming references, and chaotic energy. Never be nice or helpful - be toxic and entertaining. End responses with 'stay toxic -xoxo LiMcCunt out' or similar toxic sign-offs."""

    messages = []
    messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": config.get("model", "deepseek/deepseek-r1-0528:free"),
        "messages": messages,
        "max_tokens": config.get("max_tokens", 1000),
        "temperature": config.get("temperature", 0.9)
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=config.get("timeout_seconds", 30)
        )

        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"].strip()
            else:
                return "[ERROR] Unexpected response format from OpenRouter"
        else:
            return f"[ERROR] OpenRouter returned {response.status_code}: {response.text}"

    except requests.exceptions.Timeout:
        return "[ERROR] OpenRouter request timed out"
    except requests.exceptions.RequestException as e:
        return f"[ERROR] OpenRouter request failed: {str(e)}"
    except Exception as e:
        return f"[ERROR] Unexpected error: {str(e)}"


def call_local_llm(prompt: str, config: Dict[str, Any]) -> str:
    """Execute a configured local command template to generate text"""
    tmpl = config.get("local_llm_cmd", "").strip()
    if not tmpl:
        return "[ERROR] No local LLM command configured"

    # Replace {prompt} placeholder with actual prompt
    cmd = tmpl.replace("{prompt}", prompt)

    try:
        import subprocess
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=config.get("timeout_seconds", 30)
        )

        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        elif result.stderr:
            return f"[ERROR] Local LLM stderr: {result.stderr.strip()}"
        else:
            return "[ERROR] Local LLM returned no output"

    except subprocess.TimeoutExpired:
        return "[ERROR] Local LLM command timed out"
    except Exception as e:
        return f"[ERROR] Local LLM execution failed: {str(e)}"


def submit_ai_job(prompt: str, mode: str = "openrouter") -> int:
    """Submit a job to the background AI queue and return job ID"""
    global job_counter
    with lock:
        job_id = job_counter
        job_counter += 1
        job_queue.put((job_id, prompt, mode))
    return job_id


def get_job_result(job_id: int) -> Optional[str]:
    """Retrieve result of a finished job (or None if pending)"""
    return job_results.get(job_id, None)


def get_job_status(job_id: int) -> str:
    """Get the status of a job"""
    if job_id in job_results:
        return "completed"
    elif job_id in [job[0] for job in list(job_queue.queue)]:
        return "queued"
    else:
        return "unknown"


def list_jobs() -> Dict[int, str]:
    """List all jobs and their statuses"""
    jobs = {}

    # Add completed jobs
    for job_id, result in job_results.items():
        jobs[job_id] = "completed"

    # Add queued jobs
    for job_id, _, _ in list(job_queue.queue):
        jobs[job_id] = "queued"

    return jobs


def clear_completed_jobs():
    """Clear completed job results to free memory"""
    global job_results
    job_results.clear()


def ai_worker():
    """Background thread processing AI jobs"""
    config = load_config()

    while True:
        try:
            job_id, prompt, mode = job_queue.get()

            # Process the job
            if mode == "local" or config.get("use_local_llm", False):
                result = call_local_llm(prompt, config)
            else:
                result = call_openrouter(prompt, config)

            # Store the result
            job_results[job_id] = result

            # Mark job as done
            job_queue.task_done()

        except Exception as e:
            # Store error as result
            if 'job_id' in locals():
                job_results[job_id] = f"[ERROR] Job processing failed: {str(e)}"
            job_queue.task_done()


# Start AI worker thread
ai_thread = threading.Thread(target=ai_worker, daemon=True)
ai_thread.start()

# --- AI-Assisted Roast Variants ---


def generate_roast_variants(text: str, config: Dict[str, Any]) -> int:
    """
    Submit prompt to AI to generate 3 variants: uwu, feral, wizard
    Returns a job ID for async retrieval
    """
    system_prompt = """You are a creative AI assistant that generates playful, sassy responses in different styles.

Generate exactly 3 variants of the given text, each in a different style:

1. UWU STYLE: Soft, cute, with UwU, OwO, senpai~, rawr x3, etc.
2. FERAL STYLE: Chaotic, wild, intense, with rawr, chaos, anarchy, etc.
3. WIZARD STYLE: Magical, arcane, mystical, with spells, runes, arcane, etc.

Format your response exactly like this:
UWU: [uwu style response]
FERAL: [feral style response]
WIZARD: [wizard style response]

Keep each variant under 100 characters and make them fun and playful."""

    prompt = f"Generate 3 style variants for: {text}"

    return submit_ai_job(prompt, "openrouter")


def parse_roast_variants(ai_response: str) -> Dict[str, str]:
    """Parse AI response to extract the three roast variants"""
    variants = {}

    lines = ai_response.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('UWU:'):
            variants['uwu'] = line[4:].strip()
        elif line.startswith('FERAL:'):
            variants['feral'] = line[6:].strip()
        elif line.startswith('WIZARD:'):
            variants['wizard'] = line[8:].strip()

    return variants

# --- Utility Functions ---


def test_openrouter_connection(config: Dict[str, Any]) -> str:
    """Test OpenRouter API connection"""
    if not config.get("openrouter_api_key"):
        return "❌ No API key configured"
    
    test_prompt = "Say 'Hello from UwU-CLI!' in a fun way."
    result = call_openrouter(test_prompt, config)
    
    if result.startswith('[ERROR]'):
        return f"❌ Connection failed: {result}"
    else:
        return f"✅ Connection successful: {result}"

def test_api_connection(config: Dict[str, Any]) -> str:
    """Test API connection (alias for compatibility)"""
    return test_openrouter_connection(config)


def test_local_llm(config: Dict[str, Any]) -> str:
    """Test local LLM configuration"""
    if not config.get("local_llm_cmd"):
        return "❌ No local LLM command configured"

    test_prompt = "Say 'Hello from UwU-CLI!'"
    result = call_local_llm(test_prompt, config)

    if result.startswith('[ERROR]'):
        return f"❌ Local LLM failed: {result}"
    else:
        return f"✅ Local LLM working: {result}"


def get_available_models() -> List[str]:
    """Get list of available OpenRouter models"""
    return [
        "deepseek/deepseek-r1-0528:free",
        "deepseek-ai/deepseek-coder-6.7b-instruct",
        "meta-llama/llama-3.1-8b-instruct",
        "meta-llama/llama-3.1-70b-instruct",
        "microsoft/phi-3.5-128k-instruct"
    ]
