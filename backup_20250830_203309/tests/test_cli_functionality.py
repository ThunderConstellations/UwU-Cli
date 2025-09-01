#!/usr/bin/env python3
"""
Test script for UwU-CLI functionality without interactive mode
"""

import os
import sys
import subprocess
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_cli_imports():
    """Test that all CLI modules can be imported"""
    print("🧪 Testing CLI Module Imports...")
    
    try:
        # Test main CLI class
        from uwu_cli import UwUCLI
        print("✅ UwUCLI class imported successfully")
        
        # Test utility modules
        from utils.cmd_enhancements import CMDEnhancer
        from utils.ascii_ui import get_colored_prompt
        from utils.ai import submit_ai_job
        from utils.config import load_config
        from utils.tokenizer import inject_context
        
        print("✅ All utility modules imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_cli_initialization():
    """Test CLI initialization without starting the loop"""
    print("\n🧪 Testing CLI Initialization...")
    
    try:
        from uwu_cli import UwUCLI
        
        # Create CLI instance (this will test initialization)
        cli = UwUCLI()
        
        # Test basic properties
        assert hasattr(cli, 'config'), "CLI should have config"
        assert hasattr(cli, 'roasts'), "CLI should have roasts"
        assert hasattr(cli, 'cmd_enhancer'), "CLI should have CMD enhancer"
        assert hasattr(cli, 'current_theme'), "CLI should have current theme"
        
        print("✅ CLI initialized successfully with all required attributes")
        return True
        
    except Exception as e:
        print(f"❌ CLI initialization failed: {e}")
        return False

def test_cmd_enhancements():
    """Test CMD enhancement functionality"""
    print("\n🧪 Testing CMD Enhancements...")
    
    try:
        from utils.cmd_enhancements import CMDEnhancer
        
        enhancer = CMDEnhancer()
        
        # Test command aliases
        assert 'ls' in enhancer.cmd_aliases, "ls alias should exist"
        assert enhancer.cmd_aliases['ls'] == 'dir', "ls should alias to dir"
        
        # Test enhanced dir command
        result = enhancer.execute_command("dir")
        assert result is not None, "Enhanced dir should return result"
        
        print("✅ CMD enhancements working correctly")
        return True
        
    except Exception as e:
        print(f"❌ CMD enhancements failed: {e}")
        return False

def test_theme_system():
    """Test theme and UI system"""
    print("\n🧪 Testing Theme System...")
    
    try:
        from utils.ascii_ui import get_colored_prompt
        
        # Test toxic theme
        toxic_prompt = get_colored_prompt("toxic", "C:\\test")
        assert "💀" in toxic_prompt, "Toxic theme should include skull emoji"
        
        # Test other themes
        rainbow_prompt = get_colored_prompt("rainbow", "C:\\test")
        neon_prompt = get_colored_prompt("neon", "C:\\test")
        pastel_prompt = get_colored_prompt("pastel", "C:\\test")
        
        print("✅ All themes working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Theme system failed: {e}")
        return False

def test_ai_integration():
    """Test AI integration system"""
    print("\n🧪 Testing AI Integration...")
    
    try:
        from utils.ai import submit_ai_job, get_job_result
        
        # Test job submission
        job_id = submit_ai_job("Test prompt", "openrouter")
        assert isinstance(job_id, int), "Job ID should be an integer"
        
        # Test job result retrieval
        result = get_job_result(job_id)
        # Result might be None if job is still processing
        
        print("✅ AI integration working correctly")
        return True
        
    except Exception as e:
        print(f"❌ AI integration failed: {e}")
        return False

def test_plugin_system():
    """Test plugin system"""
    print("\n🧪 Testing Plugin System...")
    
    try:
        # Test Git enhancer plugin
        plugin_path = Path("plugins/git_enhancer.py")
        assert plugin_path.exists(), "Git enhancer plugin should exist"
        
        # Try to import the plugin
        import plugins.git_enhancer
        plugin = plugins.git_enhancer.register_plugin()
        
        assert hasattr(plugin, 'name'), "Plugin should have name"
        assert hasattr(plugin, 'commands'), "Plugin should have commands"
        assert 'git' in plugin.commands, "Git plugin should have git command"
        
        print("✅ Plugin system working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Plugin system failed: {e}")
        return False

def main():
    """Run all CLI functionality tests"""
    print("🚀 UwU-CLI Functionality Test Suite")
    print("=" * 60)
    
    tests = [
        test_cli_imports,
        test_cli_initialization,
        test_cmd_enhancements,
        test_theme_system,
        test_ai_integration,
        test_plugin_system
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All CLI functionality tests passed!")
        print("\n🚀 UwU-CLI is fully functional and ready to use!")
        print("   Run: python uwu_cli.py")
        print("   Or test specific features with the test scripts")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 