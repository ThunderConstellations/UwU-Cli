import os
import json
import logging

logger = logging.getLogger(__name__)

class SystemTester:
    def run_all_tests(self):
        return {"status": "success", "results": "All systems nominal"}

class ConfigurationManager:
    def __init__(self):
        self.config_path = os.path.expanduser("~/.uwu_config.json")

    def load(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}

def get_system_tester():
    return SystemTester()

def get_config_manager():
    return ConfigurationManager()
