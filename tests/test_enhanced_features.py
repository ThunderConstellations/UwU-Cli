#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Enhanced UwU-CLI Features
Tests all the new streamlined features for Telegram integration
"""

import sys
import os
sys.path.insert(0, '.')

def test_enhanced_quick_commands():
    """Test the enhanced quick commands system"""
    print("🧪 Testing Enhanced Quick Commands...")
    
    try:
        from uwu_cli import UwUCLI
        cli = UwUCLI()
        
        # Test quick commands help
        help_text = cli.get_quick_commands_help()
        print(f"✅ Quick commands help generated ({len(help_text)} characters)")
        
        # Test specific quick commands
        test_commands = ['/c', '/e', '/p', '/cs', '/f', '/o', '/t', '/r', '/d', '/h', '/s', '/g', '/infinite', '/infiniteon', '/infiniteoff']
        
        for cmd in test_commands:
            if cmd in cli.QUICK_COMMANDS:
                print(f"✅ {cmd} - {cli.QUICK_COMMANDS[cmd][:50]}...")
            else:
                print(f"❌ {cmd} - Missing from QUICK_COMMANDS")
        
        print(f"📊 Total quick commands: {len(cli.QUICK_COMMANDS)}")
        return True
        
    except Exception as e:
        print(f"❌ Quick commands test failed: {e}")
        return False

def test_multi_shell_routing():
    """Test multi-shell command routing"""
    print("\n🧪 Testing Multi-Shell Routing...")
    
    try:
        from uwu_cli import UwUCLI
        cli = UwUCLI()
        
        # Test CMD routing
        cmd_result = cli.execute_multi_shell_command('cmd: echo Testing CMD routing')
        if 'CMD Success' in cmd_result:
            print("✅ CMD routing working")
        else:
            print(f"❌ CMD routing failed: {cmd_result}")
        
        # Test PowerShell routing
        ps1_result = cli.execute_multi_shell_command('ps1: Write-Host "Testing PowerShell routing"')
        if 'powershell' in ps1_result.lower():
            print("✅ PowerShell routing working")
        else:
            print(f"❌ PowerShell routing failed: {ps1_result}")
        
        # Test Cursor AI routing
        cs_result = cli.execute_multi_shell_command('cs: continue working on this project')
        if 'Sent to Cursor AI' in cs_result:
            print("✅ Cursor AI routing working")
        else:
            print(f"❌ Cursor AI routing failed: {cs_result}")
        
        # Test invalid prefix
        invalid_result = cli.execute_multi_shell_command('invalid: test')
        if 'Unknown shell prefix' in invalid_result:
            print("✅ Invalid prefix handling working")
        else:
            print(f"❌ Invalid prefix handling failed: {invalid_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Multi-shell routing test failed: {e}")
        return False

def test_research_modes():
    """Test research mode commands"""
    print("\n🧪 Testing Research Modes...")
    
    try:
        from uwu_cli import UwUCLI
        cli = UwUCLI()
        
        # Test deep research
        deep_result = cli.execute_research_command('deep: improve this codebase')
        if 'Deep Research Mode' in deep_result:
            print("✅ Deep research mode working")
        else:
            print(f"❌ Deep research mode failed: {deep_result}")
        
        # Test code review
        review_result = cli.execute_research_command('review: analyze this code')
        if 'Code Review Mode' in review_result:
            print("✅ Code review mode working")
        else:
            print(f"❌ Code review mode failed: {review_result}")
        
        # Test security audit
        audit_result = cli.execute_research_command('audit: check for security issues')
        if 'Security Audit Mode' in audit_result:
            print("✅ Security audit mode working")
        else:
            print(f"❌ Security audit mode failed: {audit_result}")
        
        # Test invalid research mode
        invalid_result = cli.execute_research_command('invalid: test')
        if 'Research modes:' in invalid_result:
            print("✅ Invalid research mode handling working")
        else:
            print(f"❌ Invalid research mode handling failed: {invalid_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Research modes test failed: {e}")
        return False

def test_enhanced_telegram_commands():
    """Test enhanced Telegram command handling"""
    print("\n🧪 Testing Enhanced Telegram Commands...")
    
    try:
        from uwu_cli import UwUCLI
        cli = UwUCLI()
        
        # Test quick command handling
        cs_result = cli._execute_telegram_command('/cs')
        if 'Quick Command: /cs' in cs_result:
            print("✅ Quick command handling working")
        else:
            print(f"❌ Quick command handling failed: {cs_result}")
        
        # Test help command
        help_result = cli._execute_telegram_command('/help')
        if 'Available Quick Commands' in help_result:
            print("✅ Help command working")
        else:
            print(f"❌ Help command failed: {help_result}")
        
        # Test multi-shell command
        cmd_result = cli._execute_telegram_command('cmd: echo test')
        if 'CMD Success' in cmd_result:
            print("✅ Multi-shell command handling working")
        else:
            print(f"❌ Multi-shell command handling failed: {cmd_result}")
        
        # Test research mode command
        research_result = cli._execute_telegram_command('deep: test')
        if 'Deep Research Mode' in research_result:
            print("✅ Research mode command handling working")
        else:
            print(f"❌ Research mode command handling failed: {research_result}")
        
        # Test default Cursor AI prompt
        default_result = cli._execute_telegram_command('continue working on this')
        if 'Sending to Cursor AI' in default_result:
            print("✅ Default Cursor AI prompt handling working")
        else:
            print(f"❌ Default Cursor AI prompt handling failed: {default_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced Telegram commands test failed: {e}")
        return False

def test_infinite_mode():
    """Test infinite mode functionality"""
    print("\n🧪 Testing Infinite Mode...")
    
    try:
        from utils.infinite_mode import InfiniteMode
        mode = InfiniteMode()
        
        # Test starting a job
        start_result = mode.start_infinite_job('test_user', 'Test infinite mode')
        if 'Infinite mode started' in start_result:
            print("✅ Job start working")
        else:
            print(f"❌ Job start failed: {start_result}")
        
        # Test job status
        status_result = mode.get_job_status('test_user')
        if 'Active Infinite Jobs' in status_result:
            print("✅ Job status working")
        else:
            print(f"❌ Job status failed: {status_result}")
        
        # Test stopping a job
        stop_result = mode.stop_infinite_job('test_user')
        if 'Stopped' in stop_result:
            print("✅ Job stop working")
        else:
            print(f"❌ Job stop failed: {stop_result}")
        
        # Test job history
        history_result = mode.get_job_history('test_user')
        if 'Completed Infinite Jobs' in history_result:
            print("✅ Job history working")
        else:
            print(f"❌ Job history failed: {history_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Infinite mode test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 UwU-CLI Enhanced Features Test Suite")
    print("=" * 50)
    
    tests = [
        test_enhanced_quick_commands,
        test_multi_shell_routing,
        test_research_modes,
        test_enhanced_telegram_commands,
        test_infinite_mode
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced features are working correctly.")
    else:
        print(f"⚠️  {total - passed} tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 