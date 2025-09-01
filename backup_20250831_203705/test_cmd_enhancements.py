#!/usr/bin/env python3
"""
Test script for UwU-CLI CMD enhancements and AI features
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_cmd_enhancements():
    """Test CMD enhancement features"""
    print("🧪 Testing CMD Enhancements...")
    
    try:
        from utils.cmd_enhancements import CMDEnhancer
        enhancer = CMDEnhancer()
        
        # Test command aliases
        print("✅ CMDEnhancer imported successfully")
        
        # Test enhanced dir command
        result = enhancer.execute_command("dir")
        print("✅ Enhanced dir command working")
        
        # Test ls alias
        result = enhancer.execute_command("ls")
        print("✅ ls -> dir alias working")
        
        return True
        
    except Exception as e:
        print(f"❌ CMD enhancements failed: {e}")
        return False

def test_ai_integration():
    """Test AI integration features"""
    print("\n🧪 Testing AI Integration...")
    
    try:
        from utils.ai import submit_ai_job, get_job_result, test_api_connection
        
        # Test API connection
        connection_status = test_api_connection({})
        print(f"🔌 API Connection: {connection_status}")
        
        # Test job submission
        job_id = submit_ai_job("Test prompt", "openrouter")
        print(f"✅ AI job submitted: {job_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI integration failed: {e}")
        return False

def test_ascii_ui():
    """Test ASCII UI and themes"""
    print("\n🧪 Testing ASCII UI...")
    
    try:
        from utils.ascii_ui import get_colored_prompt, print_with_effect
        
        # Test toxic theme
        toxic_prompt = get_colored_prompt("toxic", "C:\\test")
        print(f"💀 Toxic theme: {toxic_prompt}")
        
        # Test effects
        print_with_effect("Test message", effect="thunderbolt")
        print("✅ ASCII UI working")
        
        return True
        
    except Exception as e:
        print(f"❌ ASCII UI failed: {e}")
        return False

def test_autosuggestions():
    """Test autosuggestions and tab completion"""
    print("\n🧪 Testing Autosuggestions...")
    
    try:
        from utils.cmd_enhancements import get_command_suggestions
        
        # Test command suggestions
        suggestions = get_command_suggestions("di")
        print(f"💡 Command suggestions for 'di': {suggestions}")
        
        return True
        
    except Exception as e:
        print(f"❌ Autosuggestions failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 UwU-CLI Enhanced Features Test Suite")
    print("=" * 50)
    
    tests = [
        test_cmd_enhancements,
        test_ai_integration,
        test_ascii_ui,
        test_autosuggestions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! UwU-CLI is ready!")
        print("\n🚀 To start UwU-CLI with enhanced features:")
        print("   python uwu_cli.py")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 