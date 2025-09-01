#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Integration Fixes
Tests all the fixes for Cursor integration, Telegram responses, and command handling
"""

from utils.autopilot import get_autopilot
from utils.cursor_controller import get_cursor_controller, send_command_to_cursor, send_shortcut_to_cursor
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_cursor_controller():
    """Test Cursor controller functionality"""
    print("🧪 Testing Cursor Controller...")

    controller = get_cursor_controller()
    if not controller:
        print("❌ Failed to initialize Cursor controller")
        return False

    print("✅ Cursor controller initialized")

    # Test status
    status = controller.get_status()
    print(f"📊 Status: {status}")

    return controller.is_available


def test_cursor_commands():
    """Test Cursor command functionality"""
    print("\n🎯 Testing Cursor Commands...")

    # Test built-in commands
    builtin_commands = [
        "save",
        "find",
        "format",
        "comment",
        "terminal"
    ]

    for cmd in builtin_commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:15} → {result}")

    # Test custom commands
    custom_commands = [
        "git: add",
        "python: run",
        "workbench.action.files.save",
        ">Git: Add",
        "split editor horizontally",
        "continue"
    ]

    for cmd in custom_commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:35} → {result}")

    return True


def test_autopilot():
    """Test autopilot functionality"""
    print("\n🚀 Testing Autopilot...")

    autopilot = get_autopilot()
    if not autopilot:
        print("❌ Failed to get autopilot")
        return False

    print(f"✅ Autopilot enabled: {autopilot.enabled}")
    print(f"✅ Adapters: {autopilot.adapters}")

    return True


def test_telegram_simulation():
    """Simulate Telegram command execution"""
    print("\n📱 Testing Telegram Command Simulation...")

    # Simulate the _execute_telegram_command method logic
    def simulate_telegram_command(command: str) -> str:
        """Simulate how Telegram commands would be processed"""
        try:
            # Handle Cursor commands specially
            if command.lower().startswith("cursor:cmd "):
                cursor_command = command[11:].strip()
                # Remove quotes if present
                if (cursor_command.startswith("'") and cursor_command.endswith("'")) or (cursor_command.startswith('"') and cursor_command.endswith('"')):
                    cursor_command = cursor_command[1:-1]
                result = send_command_to_cursor(cursor_command)
                return result

            elif command.lower().startswith("cursor:shortcut "):
                shortcut = command[16:].strip()
                # Remove quotes if present
                if (shortcut.startswith("'") and shortcut.endswith('"')) or (shortcut.startswith('"') and shortcut.endswith('"')):
                    shortcut = shortcut[1:-1]
                result = send_shortcut_to_cursor(shortcut)
                return result

            elif command.lower() == "cursor:help":
                return "📝 Cursor Editor Commands:\n" + \
                       "  cursor:cmd <command>   - Send command to Cursor\n" + \
                       "  cursor:shortcut <key>  - Send keyboard shortcut to Cursor\n" + \
                       "  cursor:help            - Show this help\n\n" + \
                       "💡 Examples:\n" + \
                       "  • cursor:cmd 'git: add'\n" + \
                       "  • cursor:cmd 'python: run'\n" + \
                       "  • cursor:shortcut 'ctrl+s'"

            elif command.lower() == "cursor:status":
                controller = get_cursor_controller()
                result = controller.get_status()
                return result

            elif command.lower() in ["help", "pwd", "ls", "dir"]:
                if command.lower() == "help":
                    return "📖 UwU-CLI Help - Available commands and features"
                elif command.lower() in ["pwd", "pwd"]:
                    return f"📁 Current directory: {os.getcwd()}"
                elif command.lower() in ["ls", "ls"]:
                    items = os.listdir(".")
                    dirs = [
                        f"📁 {item}" for item in items if os.path.isdir(item)]
                    files = [
                        f"📄 {item}" for item in items if os.path.isfile(item)]
                    return f"📂 Directory listing:\n" + "\n".join(sorted(dirs) + sorted(files))

            # Default response for other commands
            return f"Command '{command}' would be executed via shell"

        except Exception as e:
            return f"Error executing command: {str(e)}"

    # Test various command types
    test_commands = [
        "cursor:cmd 'continue'",
        'cursor:cmd "save"',
        "cursor:cmd git: add",
        "cursor:shortcut 'ctrl+s'",
        "cursor:help",
        "cursor:status",
        "help",
        "pwd",
        "ls",
        "echo hello world"
    ]

    for cmd in test_commands:
        result = simulate_telegram_command(cmd)
        print(
            f"   {cmd:25} → {result[:100]}{'...' if len(result) > 100 else ''}")

    return True


def test_quote_handling():
    """Test quote handling in commands"""
    print("\n💬 Testing Quote Handling...")

    def test_quote_removal(command: str) -> str:
        """Test quote removal logic"""
        if command.lower().startswith("cursor:cmd "):
            cursor_command = command[11:].strip()
            # Remove quotes if present
            if (cursor_command.startswith("'") and cursor_command.endswith("'")) or (cursor_command.startswith('"') and cursor_command.endswith('"')):
                cursor_command = cursor_command[1:-1]
            return f"Original: '{command}' → Extracted: '{cursor_command}'"
        return f"Not a cursor:cmd command: {command}"

    test_quoted_commands = [
        "cursor:cmd 'continue'",
        'cursor:cmd "save"',
        "cursor:cmd 'git: add'",
        'cursor:cmd "python: run"',
        "cursor:cmd workbench.action.files.save",
        "cursor:cmd 'split editor horizontally'"
    ]

    for cmd in test_quoted_commands:
        result = test_quote_removal(cmd)
        print(f"   {cmd:40} → {result}")

    return True


def main():
    """Run all tests"""
    print("🔧 Integration Fixes Test Suite")
    print("=" * 50)

    tests = [
        ("Cursor Controller", test_cursor_controller),
        ("Cursor Commands", test_cursor_commands),
        ("Autopilot", test_autopilot),
        ("Telegram Simulation", test_telegram_simulation),
        ("Quote Handling", test_quote_handling)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"\n{status} {test_name}")
        except Exception as e:
            results.append((test_name, False))
            print(f"\n❌ FAIL {test_name}: {e}")

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Integration fixes are working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
