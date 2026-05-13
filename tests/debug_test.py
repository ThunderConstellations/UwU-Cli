import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from uwu_cli import UwUCLI
cli = UwUCLI()
resp = cli._execute_telegram_command("/status")
print(f"DEBUG RESPONSE: '{resp}'")
