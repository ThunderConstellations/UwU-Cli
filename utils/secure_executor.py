import re
import os
import shlex
import subprocess
import logging

logger = logging.getLogger(__name__)

class SecureExecutor:
    def __init__(self):
        self.whitelist = ["ls", "dir", "cd", "pwd", "echo", "cat", "git", "python", "pip"]
        self.SENSITIVE_PATTERNS = [
            (r'api_key\s*=\s*[\'"][^\'"]+[\'"]', 'api_key = "***MASKED***"'),
            (r'token\s*=\s*[\'"][^\'"]+[\'"]', 'token = "***MASKED***"'),
            (r'password\s*=\s*[\'"][^\'"]+[\'"]', 'password = "***MASKED***"')
        ]

    def is_command_allowed(self, cmd_string):
        parts = shlex.split(cmd_string)
        if not parts: return False
        return parts[0].lower() in self.whitelist

    def sanitize_output(self, output):
        for pattern, replacement in self.SENSITIVE_PATTERNS:
            output = re.sub(pattern, replacement, output)
        return output

    def execute(self, cmd_string):
        if not self.is_command_allowed(cmd_string):
            return False, "Command not in whitelist"
        try:
            result = subprocess.run(cmd_string, shell=True, capture_output=True, text=True, timeout=30)
            return True, self.sanitize_output(result.stdout)
        except Exception as e:
            return False, str(e)

_executor = None
def get_secure_executor():
    global _executor
    if not _executor: _executor = SecureExecutor()
    return _executor
