#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Cursor Command Sending Features
"""

from utils.cursor_controller import get_cursor_controller, send_command_to_cursor, send_shortcut_to_cursor


def main():
    print("📝 Testing Cursor Command Sending Features...")

    # Get controller instance
    controller = get_cursor_controller()

    if not controller:
        print("❌ Failed to initialize Cursor controller")
        return

    print("✅ Cursor controller initialized")

    # Test Cursor status
    print("\n📊 Cursor Status:")
    status = controller.get_status()
    print(status)

    if not controller.is_available:
        print("\n⚠️  Cursor not available - install Cursor editor to test features")
        return

    print("\n🧪 Testing Cursor Command Sending:")

    # Test common commands
    print("\n1️⃣  Testing Common Commands:")
    commands = [
        "save",
        "find",
        "replace",
        "format",
        "comment",
        "terminal",
        "explorer",
        "settings",
        "extensions",
        "git",
        "debug",
        "run"
    ]

    for cmd in commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:15} → {result}")

    # Test shortcuts
    print("\n2️⃣  Testing Keyboard Shortcuts:")
    shortcuts = [
        "ctrl+s",
        "ctrl+f",
        "ctrl+p",
        "f5",
        "ctrl+/",
        "ctrl+shift+p",
        "ctrl+,",
        "ctrl+shift+x"
    ]

    for shortcut in shortcuts:
        result = send_shortcut_to_cursor(shortcut)
        print(f"   {shortcut:15} → {result}")

    # Test custom commands
    print("\n3️⃣  Testing Custom Commands:")
    custom_commands = [
        "Go to Symbol",
        "Toggle Sidebar",
        "Split Editor",
        "Zen Mode",
        "Toggle Fullscreen"
    ]

    for cmd in custom_commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:20} → {result}")

    print("\n🎉 Cursor command tests completed!")
    print("\n💡 Available Cursor Commands in UwU-CLI:")
    print("   • cursor:cmd <command>   - Send command to Cursor")
    print("   • cursor:shortcut <key>  - Send keyboard shortcut to Cursor")
    print("   • cursor:help            - Show detailed Cursor help")
    print("\n🚀 You can now control Cursor from UwU-CLI!")
    print("\n📱 And from Telegram! Send these commands:")
    print("   • cursor:cmd save")
    print("   • cursor:cmd format")
    print("   • cursor:shortcut ctrl+s")


if __name__ == "__main__":
    main()
