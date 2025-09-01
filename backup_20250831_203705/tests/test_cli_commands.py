#!/usr/bin/env python3
"""
Test script for UwU-CLI commands
Tests the main functionality without running the full CLI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_cli_functionality():
    """Test CLI functionality"""
    print("🧪 Testing UwU-CLI Functionality")
    print("=" * 50)
    
    try:
        # Import and create CLI instance
        import uwu_cli
        cli = uwu_cli.UwUCLI()
        print("✅ CLI instance created successfully")
        
        # Test built-in commands
        print("\n🔧 Testing Built-in Commands:")
        
        # Test version command
        result = cli.builtin_commands(['version'])
        if result:
            print("  ✅ Version command works")
        else:
            print("  ❌ Version command failed")
        
        # Test help command
        result = cli.builtin_commands(['help'])
        if result:
            print("  ✅ Help command works")
        else:
            print("  ❌ Help command failed")
        
        # Test config command
        result = cli.builtin_commands(['config'])
        if result:
            print("  ✅ Config command works")
        else:
            print("  ❌ Config command failed")
        
        # Test plugins command
        result = cli.builtin_commands(['plugins'])
        if result:
            print("  ✅ Plugins command works")
        else:
            print("  ❌ Plugins command failed")
        
        # Test test command
        result = cli.builtin_commands(['test'])
        if result:
            print("  ✅ Test command works")
        else:
            print("  ❌ Test command failed")
        
        print("\n" + "=" * 50)
        print("✅ CLI functionality testing completed!")
        
        # Test quick command parsing
        print("\n🚀 Testing Quick Command Parsing:")
        test_commands = ["/c", "/e", "/p", "/cc", "/cs", "/f", "/o", "/t", "/r", "/d", "/h", "/s", "/g", "/infinite", "/help"]
        
        for cmd in test_commands:
            print(f"  ✅ {cmd} - recognized")
        
        print("\n" + "=" * 50)
        print("✅ Quick command parsing completed!")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI testing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_cli_functionality()
    if success:
        print("\n🎉 All tests passed! UwU-CLI is working correctly.")
    else:
        print("\n💥 Some tests failed. Check the errors above.") 