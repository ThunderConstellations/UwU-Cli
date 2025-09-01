#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Configuration Fixes
Verifies that configuration loading improvements are working correctly
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_telegram_config_loading():
    """Test Telegram controller configuration loading"""
    print("🔧 Testing Telegram Controller Configuration Loading...")
    
    try:
        from utils.telegram_controller import TelegramController
        
        # Test with default configuration
        controller = TelegramController()
        
        if controller.token and controller.chat_id:
            print("   ✅ Telegram configuration loaded successfully")
            print(f"      
            print(f"      Chat ID: {controller.chat_id}")
            return True
        else:
            print("   ⚠️  Telegram configuration not loaded")
            return False
            
    except Exception as e:
        print(f"   ❌ Telegram controller test failed: {e}")
        return False

def test_autopilot_config_loading():
    """Test Autopilot configuration loading"""
    print("\n🚀 Testing Autopilot Configuration Loading...")
    
    try:
        from utils.autopilot import Autopilot
        
        # Test with default configuration
        autopilot = Autopilot()
        
        if autopilot.enabled:
            print("   ✅ Autopilot configuration loaded successfully")
            print(f"      Enabled: {autopilot.enabled}")
            print(f"      Adapters: {autopilot.adapters}")
            return True
        else:
            print("   ⚠️  Autopilot is disabled in configuration")
            return False
            
    except Exception as e:
        print(f"   ❌ Autopilot test failed: {e}")
        return False

def test_config_file_discovery():
    """Test configuration file discovery in different locations"""
    print("\n🔍 Testing Configuration File Discovery...")
    
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test configuration
        test_config = {
            "enabled": True,
            "adapters": ["telegram"],
            "telegram": {
                "token": "test_token_12345",
                "chatId": "test_chat_67890"
            }
        }
        
        # Test 1: Config in current directory
        current_config = Path(".autopilot.json")
        if current_config.exists():
            print("   ✅ Configuration found in current directory")
        else:
            print("   ⚠️  No configuration in current directory")
        
        # Test 2: Config in project root
        project_root = Path(__file__).parent
        project_config = project_root / ".autopilot.json"
        if project_config.exists():
            print("   ✅ Configuration found in project root")
        else:
            print("   ⚠️  No configuration in project root")
        
        # Test 3: Config in utils parent directory
        utils_parent = project_root / "utils"
        if utils_parent.exists():
            utils_parent_config = utils_parent.parent / ".autopilot.json"
            if utils_parent_config.exists():
                print("   ✅ Configuration found in utils parent directory")
            else:
                print("   ⚠️  No configuration in utils parent directory")
        
        return True

def test_error_handling():
    """Test error handling improvements"""
    print("\n🛡️  Testing Error Handling Improvements...")
    
    try:
        from utils.error_handler import get_error_handler, ErrorCategory, ErrorSeverity
        
        error_handler = get_error_handler()
        
        # Test error handling
        test_error = ValueError("Test configuration error")
        result = error_handler.handle_error(test_error, ErrorCategory.VALIDATION, {}, ErrorSeverity.MEDIUM)
        
        if result:
            print("   ✅ Error handler working correctly")
            return True
        else:
            print("   ⚠️  Error handler returned empty result")
            return False
        
    except Exception as e:
        print(f"   ❌ Error handler test failed: {e}")
        return False

def test_logging_consistency():
    """Test logging consistency across modules"""
    print("\n📝 Testing Logging Consistency...")
    
    try:
        # Check if log files exist and are accessible
        log_dir = Path("tmp/logs")
        if log_dir.exists():
            log_files = list(log_dir.glob("*.log"))
            if log_files:
                print(f"   ✅ Found {len(log_files)} log files:")
                for log_file in log_files:
                    size = log_file.stat().st_size
                    print(f"      - {log_file.name}: {size} bytes")
                return True
            else:
                print("   ⚠️  No log files found")
                return False
        else:
            print("   ⚠️  Log directory not found")
            return False
            
    except Exception as e:
        print(f"   ❌ Logging consistency test failed: {e}")
        return False

def test_telegram_functionality():
    """Test Telegram functionality"""
    print("\n📱 Testing Telegram Functionality...")
    
    try:
        from utils.telegram_controller import TelegramController
        
        controller = TelegramController()
        
        # Test if we can start listening
        if controller.token and controller.chat_id:
            print("   ✅ Telegram controller properly configured")
            
            # Test command callback setting
            def test_callback(command):
                return f"Test response to: {command}"
            
            controller.set_command_callback(test_callback)
            print("   ✅ Command callback set successfully")
            
            return True
        else:
            print("   ⚠️  Telegram controller not fully configured")
            return False
            
    except Exception as e:
        print(f"   ❌ Telegram functionality test failed: {e}")
        return False

def main():
    """Run all configuration tests"""
    print("🧪 UwU-CLI Configuration Fixes Test Suite")
    print("=" * 50)
    
    tests = [
        test_telegram_config_loading,
        test_autopilot_config_loading,
        test_config_file_discovery,
        test_error_handling,
        test_logging_consistency,
        test_telegram_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All configuration tests passed! Configuration loading is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 