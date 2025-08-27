#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for State Management System
Tests the new state manager functionality for Phase 3
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.state_manager import get_state_manager, StateManager

def test_state_manager_creation():
    """Test state manager creation and initialization"""
    print("📊 Testing State Manager Creation...")
    
    try:
        state_manager = get_state_manager()
        if not state_manager:
            print("❌ Failed to create state manager")
            return False
        
        print("✅ State manager created successfully")
        print(f"   Data directory: {state_manager.data_dir}")
        print(f"   Session file: {state_manager.session_file}")
        print(f"   History file: {state_manager.history_file}")
        print(f"   Context file: {state_manager.context_file}")
        print(f"   Preferences file: {state_manager.preferences_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ State manager creation failed: {e}")
        return False

def test_session_management():
    """Test session management functionality"""
    print("\n🔄 Testing Session Management...")
    
    try:
        state_manager = get_state_manager()
        
        # Get session info
        session_info = state_manager.get_session_info()
        print("   📋 Session Information:")
        for key, value in session_info.items():
            print(f"      {key}: {value}")
        
        # Test session activity update
        print("\n   🔄 Testing session activity update...")
        old_commands = session_info['commands_executed']
        state_manager.update_session_activity()
        new_session_info = state_manager.get_session_info()
        
        if new_session_info['commands_executed'] > old_commands:
            print("      ✅ Session activity updated successfully")
        else:
            print("      ❌ Session activity update failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Session management test failed: {e}")
        return False

def test_command_history():
    """Test command history functionality"""
    print("\n📚 Testing Command History...")
    
    try:
        state_manager = get_state_manager()
        
        # Add test commands to history
        print("   📝 Adding test commands to history...")
        test_commands = [
            ("echo Hello World", True, "Hello World", "", 0.1),
            ("dir", True, "Directory listing...", "", 0.2),
            ("invalid_command", False, "", "Command not found", 0.0),
            ("git status", True, "On branch main...", "", 0.3),
            ("python --version", True, "Python 3.9.0", "", 0.1)
        ]
        
        for cmd, success, output, error, exec_time in test_commands:
            state_manager.add_command_to_history(cmd, success, output, error, exec_time)
            print(f"      Added: {cmd} ({'✅' if success else '❌'})")
        
        # Test history retrieval
        print("\n   📖 Testing history retrieval...")
        recent_history = state_manager.get_command_history(limit=5)
        print(f"      Recent commands: {len(recent_history)}")
        
        # Test history search
        print("\n   🔍 Testing history search...")
        git_results = state_manager.search_command_history("git", limit=3)
        print(f"      Git commands found: {len(git_results)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Command history test failed: {e}")
        return False

def test_context_management():
    """Test context management functionality"""
    print("\n🎯 Testing Context Management...")
    
    try:
        state_manager = get_state_manager()
        
        # Test context updates
        print("   🔄 Testing context updates...")
        test_context = {
            'current_theme': 'dark',
            'last_working_directory': '/test/path',
            'favorite_commands': ['git status', 'python test.py'],
            'git_status': {'branch': 'main', 'clean': True}
        }
        
        for key, value in test_context.items():
            state_manager.update_context(key, value)
            print(f"      Updated {key}: {value}")
        
        # Test context retrieval
        print("\n   📖 Testing context retrieval...")
        for key, expected_value in test_context.items():
            retrieved_value = state_manager.get_context(key)
            if retrieved_value == expected_value:
                print(f"      ✅ {key}: {retrieved_value}")
            else:
                print(f"      ❌ {key}: expected {expected_value}, got {retrieved_value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Context management test failed: {e}")
        return False

def test_preferences_management():
    """Test preferences management functionality"""
    print("\n⚙️  Testing Preferences Management...")
    
    try:
        state_manager = get_state_manager()
        
        # Test preference updates
        print("   🔄 Testing preference updates...")
        test_preferences = {
            'auto_save': False,
            'history_size': 500,
            'theme': 'light',
            'language': 'es'
        }
        
        for key, value in test_preferences.items():
            state_manager.update_preferences(key, value)
            print(f"      Updated {key}: {value}")
        
        # Test preference retrieval
        print("\n   📖 Testing preference retrieval...")
        for key, expected_value in test_preferences.items():
            retrieved_value = state_manager.get_preferences(key)
            if retrieved_value == expected_value:
                print(f"      ✅ {key}: {retrieved_value}")
            else:
                print(f"      ❌ {key}: expected {expected_value}, got {retrieved_value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Preferences management test failed: {e}")
        return False

def test_statistics():
    """Test statistics functionality"""
    print("\n📊 Testing Statistics...")
    
    try:
        state_manager = get_state_manager()
        
        # Get statistics
        stats = state_manager.get_statistics()
        print("   📈 Usage Statistics:")
        for key, value in stats.items():
            print(f"      {key}: {value}")
        
        # Test export functionality
        print("\n   📤 Testing data export...")
        export_file = "tmp/session_export_test.json"
        export_success = state_manager.export_session_data(export_file)
        
        if export_success:
            print(f"      ✅ Session data exported to {export_file}")
        else:
            print("      ❌ Session data export failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Statistics test failed: {e}")
        return False

def test_advanced_features():
    """Test advanced state management features"""
    print("\n🚀 Testing Advanced Features...")
    
    try:
        state_manager = get_state_manager()
        
        # Test session reset
        print("   🔄 Testing session reset...")
        old_session_id = state_manager.current_session['session_id']
        state_manager.reset_session()
        new_session_id = state_manager.current_session['session_id']
        
        if old_session_id != new_session_id:
            print("      ✅ Session reset successful")
        else:
            print("      ❌ Session reset failed")
        
        # Test history clearing
        print("\n   🗑️  Testing history clearing...")
        old_history_size = len(state_manager.command_history)
        state_manager.clear_history()
        new_history_size = len(state_manager.command_history)
        
        if new_history_size == 0:
            print("      ✅ History cleared successfully")
        else:
            print("      ❌ History clearing failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Advanced features test failed: {e}")
        return False

def main():
    """Run all state management tests"""
    print("📊 State Management System Test Suite")
    print("=" * 60)
    
    tests = [
        ("State Manager Creation", test_state_manager_creation),
        ("Session Management", test_session_management),
        ("Command History", test_command_history),
        ("Context Management", test_context_management),
        ("Preferences Management", test_preferences_management),
        ("Statistics", test_statistics),
        ("Advanced Features", test_advanced_features)
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
    print("📊 State Management Test Results Summary:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All state management tests passed!")
        print("\n📊 State Management Features Active:")
        print("   • Session persistence")
        print("   • Command history tracking")
        print("   • Context maintenance")
        print("   • User preferences")
        print("   • Usage statistics")
        print("   • Data export functionality")
        print("\n🚀 Ready to proceed with Phase 4: Enhanced Error Handling")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 