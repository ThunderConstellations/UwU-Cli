import os
import json
import logging
import requests
import threading
import time

logger = logging.getLogger(__name__)

class TelegramController:
    def __init__(self):
        self.token = None
        self.chat_id = None
        self.last_update_id = 0
        self.is_listening = False
        self.command_callback = None

    def load_config(self, config_path):
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                cfg = json.load(f).get("telegram", {})
                self.token = cfg.get("token")
                self.chat_id = cfg.get("chatId")
        return self.token and self.chat_id

    def send_message(self, text):
        if not self.token or not self.chat_id: return False
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            requests.post(url, json={"chat_id": self.chat_id, "text": text}, timeout=10)
            return True
        except: return False

_controller = None
def get_telegram_controller():
    global _controller
    if not _controller: _controller = TelegramController()
    return _controller

def start_telegram_control(callback):
    ctrl = get_telegram_controller()
    ctrl.command_callback = callback
    return True

def stop_telegram_control():
    pass
