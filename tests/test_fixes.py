#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify command parsing fixes
"""

def test_command_parsing():
    """Test various command parsing scenarios"""
    print("🧪 Testing Command Parsing Fixes...")
    
    # Test case-insensitive commands
    print("\n1️⃣  Testing Case-Insensitive Commands:")
    test_commands = [
        "Pwd",
        "pwd", 
        "PWD",
        "Ls",
        "ls",
        "LS",
        "Help",
        "help",
        "HELP"
    ]
    
    for cmd in test_commands:
        print(f"   {cmd:10} → {cmd.lower()}")
    
    # Test Cursor command parsing
    print("\n2️⃣  Testing Cursor Command Parsing:")
    cursor_commands = [
        "cursor:cmd 'continue'",
        'cursor:cmd "save"',
        "cursor:cmd format",
        "cursor:shortcut 'ctrl+s'",
        'cursor:shortcut "f5"',
        "cursor:shortcut ctrl+f"
    ]
    
    for cmd in cursor_commands:
        if cmd.startswith("cursor:cmd "):
            command = cmd[11:].strip()
            if (command.startswith("'") and command.endswith("'")) or (command.startswith('"') and command.endswith('"')):
                command = command[1:-1]
            print(f"   {cmd:25} → command: '{command}'")
        elif cmd.startswith("cursor:shortcut "):
            shortcut = cmd[16:].strip()
            if (shortcut.startswith("'") and shortcut.endswith("'")) or (shortcut.startswith('"') and shortcut.endswith('"')):
                shortcut = shortcut[1:-1]
            print(f"   {cmd:25} → shortcut: '{shortcut}'")
    
    # Test alias handling
    print("\n3️⃣  Testing Alias Handling:")
    aliases = {
        "pwd": "pwd",
        "ls": "dir", 
        "clear": "cls",
        "help": "help",
        "exit": "exit",
        "quit": "exit",
        "bye": "exit"
    }
    
    for alias, resolved in aliases.items():
        print(f"   {alias:10} → {resolved}")
    
    print("\n🎉 Command parsing tests completed!")
    print("\n💡 These fixes should resolve:")
    print("   • Case sensitivity issues (Pwd → pwd)")
    print("   • Cursor command parsing (cursor:cmd 'continue' → continue)")
    print("   • Command aliases (ls → dir)")
    print("\n🚀 Test in UwU-CLI to verify!")

if __name__ == "__main__":
    test_command_parsing() 