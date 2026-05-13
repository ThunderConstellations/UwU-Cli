import os
import json
import logging
import requests
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class Autopilot:
    def __init__(self):
        self.config = self._load_config()
        self.enabled = self.config.get("enabled", True)
        self.adapters = self.config.get("adapters", ["telegram"])

    def _load_config(self) -> Dict[str, Any]:
        path = os.path.expanduser("~/.autopilot.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    def send_notification(self, message: str, title: str = "UwU-CLI") -> bool:
        if not self.enabled: return False
        success = True
        if "telegram" in self.adapters:
            success = success and self._send_telegram(message)
        return success

    def _send_telegram(self, message: str) -> bool:
        token = self.config.get("telegram", {}).get("token")
        chat_id = self.config.get("telegram", {}).get("chatId")
        if not token or not chat_id: return False
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, json={"chat_id": chat_id, "text": message}, timeout=10)
            return True
        except: return False

def get_autopilot():
    return Autopilot()

def send_notification(message, title="UwU-CLI"):
    return get_autopilot().send_notification(message, title)
