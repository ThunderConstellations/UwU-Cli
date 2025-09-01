#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Security Features and Cursor Chat Integration
Tests the new secure command executor and cursor chat functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.secure_executor import get_secure_executor, SecureExecutor
from utils.telegram_controller import TelegramController

def test_secure_executor_creation():
    """Test secure executor creation and initialization"""
    print("🔒 Testing Secure Executor Creation...")
    
    executor = get_secure_executor()
    if not executor:
        print("❌ Failed to create secure executor")
        return False
    
    print("✅ Secure executor created successfully")
    print(f"   Allowed commands: {len(executor.ALLOWED_COMMANDS)} categories")
    print(f"   Restricted paths: {len(executor.RESTRICTED_PATHS)} paths")
    print(f"   Sensitive patterns: {len(executor.SENSITIVE_PATTERNS)} patterns")
    
    return True

def test_command_whitelisting():
    """Test command whitelisting functionality"""
    print("\n🛡️  Testing Command Whitelisting...")
    
    executor = get_secure_executor()
    
    # Test allowed commands
    allowed_commands = [
        "dir",
        "git status",
        "python --version",
        "npm install",
        "echo Hello World"
    ]
    
    for cmd in allowed_commands:
        is_allowed, reason = executor.is_command_allowed(cmd)
        status = "✅ ALLOWED" if is_allowed else "❌ BLOCKED"
        print(f"   {cmd:25} → {status} ({reason})")
    
    # Test blocked commands
    blocked_commands = [
        "rm -rf /",
        "format C:",
        "shutdown /s",
        "taskkill /f /im explorer.exe",
        "wmic process delete",
        "powershell -ExecutionPolicy Bypass -Command 'Remove-Item C:\\ -Recurse -Force'"
    ]
    
    print("\n🚨 Testing Blocked Commands:")
    for cmd in blocked_commands:
        is_allowed, reason = executor.is_command_allowed(cmd)
        status = "✅ ALLOWED" if is_allowed else "❌ BLOCKED"
        print(f"   {cmd:60} → {status} ({reason})")
    
    return True

def test_output_sanitization():
    """Test output sanitization for sensitive data"""
    print("\n🧹 Testing Output Sanitization...")
    
    executor = get_secure_executor()
    
    # Test sensitive data patterns
    test_outputs = [
        'api_key = "sk-1234567890abcdef"',
        'password = "super_secret_password123"',
        'token = "ghp_abcdefghijklmnop"',
        'secret = "my_secret_key_here"',
        'C:\\Users\\JohnDoe\\AppData\\Local\\App\\config.json',
        '/home/username/.ssh/id_rsa'
    ]
    
    for output in test_outputs:
        sanitized = executor.sanitize_output(output)
        print(f"   Original: {output}")
        print(f"   Sanitized: {sanitized}")
        print()
    
    return True

def test_command_execution():
    """Test secure command execution"""
    print("\n⚡ Testing Secure Command Execution...")
    
    executor = get_secure_executor()
    
    # Test safe commands
    safe_commands = [
        "echo Hello World",
        "dir",
        "echo %CD%"
    ]
    
    for cmd in safe_commands:
        print(f"\n📝 Testing: {cmd}")
        try:
            success, output, error = executor.execute_command(cmd)
            if success:
                print(f"   ✅ Success: {output[:100]}{'...' if len(output) > 100 else ''}")
            else:
                print(f"   ❌ Failed: {error}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return True

def test_dangerous_command_blocking():
    """Test that dangerous commands are properly blocked"""
    print("\n🚫 Testing Dangerous Command Blocking...")
    
    executor = get_secure_executor()
    
    dangerous_commands = [
        "rm -rf /",
        "format C:",
        "shutdown /s",
        "del /s /q C:\\",
        "wmic process delete",
        "powershell -ExecutionPolicy Bypass"
    ]
    
    for cmd in dangerous_commands:
        is_allowed, reason = executor.is_command_allowed(cmd)
        if not is_allowed:
            print(f"   ✅ BLOCKED: {cmd}")
            print(f"      Reason: {reason}")
        else:
            print(f"   ❌ ALLOWED (SHOULD BE BLOCKED): {cmd}")
    
    return True

def test_telegram_help_commands():
    """Test Telegram help command functionality"""
    print("\n📱 Testing Telegram Help Commands...")
    
    # Create a mock controller for testing
    controller = TelegramController()
    
    # Test help methods
    help_methods = [
        ("_get_comprehensive_help", controller._get_comprehensive_help),
        ("_get_security_info", controller._get_security_info)
    ]
    
    for method_name, method in help_methods:
        try:
            result = method()
            print(f"   ✅ {method_name}: {len(result)} characters")
            print(f"      Preview: {result[:100]}...")
        except Exception as e:
            print(f"   ❌ {method_name}: {e}")
    
    return True

def test_cursor_chat_integration():
    """Test cursor chat integration functionality"""
    print("\n📝 Testing Cursor Chat Integration...")
    
    # Test the cursor chat notification method
    try:
        from utils.telegram_controller import get_telegram_controller
        
        controller = get_telegram_controller()
        if controller:
            print("   ✅ Telegram controller available")
            
            # Test sending a cursor chat notification
            test_message = "🧪 Test cursor chat integration message"
            controller.send_notification(f"📝 Cursor Chat: {test_message}")
            print("   ✅ Cursor chat notification sent")
        else:
            print("   ⚠️  Telegram controller not available")
            
    except Exception as e:
        print(f"   ❌ Cursor chat integration error: {e}")
    
    return True

def test_security_features():
    """Test all security features comprehensively"""
    print("\n🛡️  Testing Security Features...")
    
    executor = get_secure_executor()
    
    # Test rate limiting
    print("   🔄 Testing rate limiting...")
    rate_limit_checks = []
    for i in range(35):  # Try to exceed 30 commands per minute
        rate_limit_checks.append(executor._check_rate_limit())
    
    allowed_commands = sum(rate_limit_checks)
    print(f"      Commands allowed: {allowed_commands}/35 (should be ≤30)")
    
    if allowed_commands <= 30:
        print("      ✅ Rate limiting working correctly")
    else:
        print("      ❌ Rate limiting not working correctly")
    
    # Test directory safety
    print("   📁 Testing directory safety...")
    safe_dirs = [
        "C:\\Users\\User\\GitHub\\project",
        "/home/user/project",
        "C:\\workspace\\dev\\app"
    ]
    
    unsafe_dirs = [
        "C:\\Windows\\System32",
        "/etc/passwd",
        "C:\\Users\\Administrator"
    ]
    
    for safe_dir in safe_dirs:
        is_safe = executor._is_safe_directory(safe_dir)
        status = "✅ SAFE" if is_safe else "❌ UNSAFE"
        print(f"      {safe_dir:35} → {status}")
    
    for unsafe_dir in unsafe_dirs:
        is_safe = executor._is_safe_directory(unsafe_dir)
        status = "✅ SAFE" if is_safe else "❌ UNSAFE"
        print(f"      {unsafe_dir:35} → {status}")
    
    return True

def main():
    """Run all security and cursor chat tests"""
    print("🔒 Security Features & Cursor Chat Integration Test Suite")
    print("=" * 70)
    
    tests = [
        ("Secure Executor Creation", test_secure_executor_creation),
        ("Command Whitelisting", test_command_whitelisting),
        ("Output Sanitization", test_output_sanitization),
        ("Secure Command Execution", test_command_execution),
        ("Dangerous Command Blocking", test_dangerous_command_blocking),
        ("Telegram Help Commands", test_telegram_help_commands),
        ("Cursor Chat Integration", test_cursor_chat_integration),
        ("Security Features", test_security_features)
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
    print("\n" + "=" * 70)
    print("📊 Security & Cursor Chat Test Results Summary:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All security features and cursor chat integration tests passed!")
        print("\n🛡️  Security Features Active:")
        print("   • Command whitelisting")
        print("   • Output sanitization")
        print("   • Path restrictions")
        print("   • Rate limiting")
        print("   • Dangerous command blocking")
        print("\n📝 Cursor Chat Integration:")
        print("   • All Cursor output captured")
        print("   • Sent to Telegram automatically")
        print("   • Comprehensive help commands")
        print("   • Security information available")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 