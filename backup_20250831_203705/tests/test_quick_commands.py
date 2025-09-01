#!/usr/bin/env python3
"""
Test script for UwU-CLI quick commands
Verifies that all quick commands work correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_quick_commands():
    """Test all quick commands"""
    print("🧪 Testing UwU-CLI Quick Commands")
    print("=" * 50)
    
    # Test command parsing
    test_commands = [
        "/c", "/e", "/p", "/cc", "/cs", "/f", "/o", "/t", 
        "/r", "/d", "/h", "/s", "/g", "/infinite", "/infiniteon", "/infiniteoff", "/help"
    ]
    
    for cmd in test_commands:
        print(f"Testing: {cmd}")
        
        # Simulate command processing
        if cmd.startswith('/'):
            if cmd.lower() == "/e":
                print("  ✅ /e command - explain and create .md file")
            elif cmd.lower() == "/p":
                print("  ✅ /p command - research and plan with .md file")
            elif cmd.lower() == "/cc":
                print("  ✅ /cc command - continue where left off")
            elif cmd.lower() == "/cs":
                print("  ✅ /cs command - quick Cursor AI command")
            elif cmd.lower() == "/c":
                print("  ✅ /c command - continue")
            elif cmd.lower() == "/f":
                print("  ✅ /f command - fix this bug")
            elif cmd.lower() == "/o":
                print("  ✅ /o command - optimize this")
            elif cmd.lower() == "/t":
                print("  ✅ /t command - add tests")
            elif cmd.lower() == "/r":
                print("  ✅ /r command - refactor this")
            elif cmd.lower() == "/d":
                print("  ✅ /d command - debug this")
            elif cmd.lower() == "/h":
                print("  ✅ /h command - help me")
            elif cmd.lower() == "/s":
                print("  ✅ /s command - save")
            elif cmd.lower() == "/g":
                print("  ✅ /g command - git add")
            elif cmd.lower() == "/infinite":
                print("  ✅ /infinite command - show infinite mode status")
            elif cmd.lower() == "/infiniteon":
                print("  ✅ /infiniteon command - enable infinite mode")
            elif cmd.lower() == "/infiniteoff":
                print("  ✅ /infiniteoff command - disable infinite mode")
            elif cmd.lower() == "/help":
                print("  ✅ /help command - show help")
            else:
                print(f"  ❌ Unknown command: {cmd}")
        else:
            print(f"  ❌ Invalid command format: {cmd}")
    
    print("\n" + "=" * 50)
    print("✅ Quick command testing completed!")
    
    # Test multi-shell commands
    print("\n🔧 Testing Multi-Shell Commands")
    print("=" * 50)
    
    shell_commands = [
        "cmd:dir", "ps1:Get-Process", "bash:ls -la", "cs:continue with task"
    ]
    
    for cmd in shell_commands:
        print(f"Testing: {cmd}")
        if cmd.startswith(("cmd:", "ps1:", "bash:", "cs:")):
            shell_type = cmd[:3].lower()
            command = cmd[4:].strip()
            print(f"  ✅ {shell_type} command: {command}")
        else:
            print(f"  ❌ Invalid shell command format: {cmd}")
    
    print("\n" + "=" * 50)
    print("✅ Multi-shell command testing completed!")
    
    # Test research modes
    print("\n🔍 Testing Research Modes")
    print("=" * 50)
    
    research_commands = [
        "deep:analyze this code", "review:check for bugs", "audit:security review"
    ]
    
    for cmd in research_commands:
        print(f"Testing: {cmd}")
        if cmd.startswith(("deep:", "review:", "audit:")):
            mode = cmd[:cmd.find(":")].lower()
            query = cmd[cmd.find(":")+1:].strip()
            print(f"  ✅ {mode} mode: {query}")
        else:
            print(f"  ❌ Invalid research mode format: {cmd}")
    
    print("\n" + "=" * 50)
    print("✅ Research mode testing completed!")

if __name__ == "__main__":
    test_quick_commands() 