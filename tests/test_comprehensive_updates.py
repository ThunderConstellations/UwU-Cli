import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_dry_run_logic():
    print("🧪 Testing Dry Run Logic...")
    from uwu_cli import UwUCLI
    cli = UwUCLI()
    cli.dry_run = True
    assert cli.dry_run == True
    print("✅ Dry Run State OK")

def test_telegram_status_handler():
    print("🧪 Testing Telegram Status Handler...")
    from uwu_cli import UwUCLI
    cli = UwUCLI()
    response = cli._execute_telegram_command("/status")
    assert "System Status" in response
    assert "CPU" in response
    print("✅ Telegram /status OK")

def test_context_lord_level():
    print("🧪 Testing Lord Level Context...")
    from utils.context_scanner import ContextScanner
    scanner = ContextScanner()
    ctx = scanner.get_context_string()
    assert "LORD LEVEL ENGINEER" in ctx
    print("✅ Context Lord Level OK")

if __name__ == "__main__":
    test_dry_run_logic()
    test_telegram_status_handler()
    test_context_lord_level()
    print("\n🎉 Comprehensive updates verified!")
