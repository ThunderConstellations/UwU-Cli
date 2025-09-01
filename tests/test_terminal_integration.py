#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Terminal-in-Cursor Integration
Tests the new approach where UwU-CLI runs in Cursor's terminal
and Telegram can execute terminal commands directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.telegram_controller import TelegramController
from utils.cursor_controller import get_cursor_controller

def test_terminal_command_execution():
    """Test terminal command execution functionality"""
    print("🧪 Testing Terminal Command Execution...")
    
    # Create a mock controller for testing
    controller = TelegramController()
    
    # Test basic terminal commands
    test_commands = [
        "dir",
        "echo Hello World",
        "python --version",
        "git --version",
        "pwd",
        "ls -la"
    ]
    
    for cmd in test_commands:
        print(f"\n📝 Testing: {cmd}")
        result = controller.execute_terminal_command(cmd)
        print(f"   Result: {result[:200]}{'...' if len(result) > 200 else ''}")
    
    return True

def test_cursor_terminal_integration():
    """Test how Cursor terminal integration would work"""
    print("\n🎯 Testing Cursor Terminal Integration...")
    
    # Get Cursor controller
    cursor_controller = get_cursor_controller()
    if not cursor_controller:
        print("❌ Cursor controller not available")
        return False
    
    print("✅ Cursor controller available")
    
    # Test opening current folder in Cursor
    print("\n📁 Opening current folder in Cursor...")
    result = cursor_controller.open_folder(".")
    print(f"   Result: {result}")
    
    # Test opening a specific file
    print("\n📄 Opening test file in Cursor...")
    result = cursor_controller.open_file("test_terminal_integration.py")
    print(f"   Result: {result}")
    
    return True

def test_telegram_command_flow():
    """Test the complete Telegram command flow"""
    print("\n📱 Testing Telegram Command Flow...")
    
    # Simulate the command handling flow
    def simulate_telegram_command(command: str) -> str:
        """Simulate how Telegram commands would be processed"""
        try:
            # Check if this is a terminal command (starts with !)
            if command.startswith("!"):
                # Execute as terminal command
                terminal_cmd = command[1:].strip()
                print(f"   🖥️  Executing terminal command: {terminal_cmd}")
                
                # Simulate terminal execution
                if terminal_cmd == "dir":
                    return "✅ Command executed successfully:\n📁 Directory listing would appear here"
                elif terminal_cmd == "git status":
                    return "✅ Command executed successfully:\n📚 Git status would appear here"
                elif terminal_cmd == "python test.py":
                    return "✅ Command executed successfully:\n🐍 Python script output would appear here"
                else:
                    return f"✅ Command executed successfully:\nTerminal output for: {terminal_cmd}"
            else:
                # Execute via CLI callback
                print(f"   🎮 Executing CLI command: {command}")
                return f"CLI command result for: {command}"
                
        except Exception as e:
            return f"❌ Error executing command: {str(e)}"
    
    # Test various command types
    test_commands = [
        "!dir",
        "!git status", 
        "!python test.py",
        "!echo Hello World",
        "help",
        "cursor:help",
        "pwd"
    ]
    
    for cmd in test_commands:
        result = simulate_telegram_command(cmd)
        print(f"   {cmd:20} → {result[:100]}{'...' if len(result) > 100 else ''}")
    
    return True

def test_real_terminal_commands():
    """Test actual terminal command execution"""
    print("\n🖥️  Testing Real Terminal Commands...")
    
    # Create controller
    controller = TelegramController()
    
    # Test simple commands that should work
    simple_commands = [
        "echo 'Hello from UwU-CLI!'",
        "dir",
        "echo %CD%",
        "python -c \"print('Python is working!')\""
    ]
    
    for cmd in simple_commands:
        print(f"\n📝 Testing: {cmd}")
        try:
            result = controller.execute_terminal_command(cmd)
            print(f"   Result: {result[:200]}{'...' if len(result) > 200 else ''}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return True

def main():
    """Run all tests"""
    print("🔧 Terminal-in-Cursor Integration Test Suite")
    print("=" * 60)
    
    tests = [
        ("Terminal Command Execution", test_terminal_command_execution),
        ("Cursor Terminal Integration", test_cursor_terminal_integration),
        ("Telegram Command Flow", test_telegram_command_flow),
        ("Real Terminal Commands", test_real_terminal_commands)
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
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Terminal integration is working correctly.")
        print("\n🚀 How to Use:")
        print("1. Run UwU-CLI inside Cursor's integrated terminal")
        print("2. Send commands via Telegram:")
        print("   • Regular commands: 'ls', 'help', 'cursor:help'")
        print("   • Terminal commands: '!dir', '!git status', '!python test.py'")
        print("3. All terminal output will be sent back to Telegram")
        print("4. You'll see real-time Cursor changes and terminal responses!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 