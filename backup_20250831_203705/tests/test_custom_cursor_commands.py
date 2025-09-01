#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Custom Cursor Commands
"""

from utils.cursor_controller import get_cursor_controller, send_command_to_cursor, send_shortcut_to_cursor

def main():
    print("🎯 Testing Custom Cursor Commands...")
    
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
    
    print("\n🧪 Testing Custom Cursor Commands:")
    
    # Test built-in commands
    print("\n1️⃣  Built-in Commands:")
    builtin_commands = [
        "save",
        "find", 
        "format",
        "comment",
        "terminal",
        "explorer"
    ]
    
    for cmd in builtin_commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:15} → {result}")
    
    # Test internal Cursor commands
    print("\n2️⃣  Internal Cursor Commands:")
    internal_commands = [
        "workbench.action.files.save",
        "editor.action.formatDocument",
        "view.explorer",
        "workbench.action.toggleSidebar",
        "editor.action.commentLine"
    ]
    
    for cmd in internal_commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:35} → {result}")
    
    # Test extension commands
    print("\n3️⃣  Extension Commands:")
    extension_commands = [
        "git.add",
        "python.runFile",
        "extension.install",
        "git.commit",
        "python.debugFile"
    ]
    
    for cmd in extension_commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:20} → {result}")
    
    # Test command palette commands
    print("\n4️⃣  Command Palette Commands:")
    palette_commands = [
        ">Git: Add",
        ">Python: Run File",
        ">File: Open File",
        ">View: Toggle Explorer",
        ">Terminal: Create New Terminal"
    ]
    
    for cmd in palette_commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:30} → {result}")
    
    # Test Git commands
    print("\n5️⃣  Git Commands:")
    git_commands = [
        "git: add",
        "git: commit",
        "git: push",
        "git: pull",
        "git: status"
    ]
    
    for cmd in git_commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:20} → {result}")
    
    # Test Python/Debug commands
    print("\n6️⃣  Python/Debug Commands:")
    python_commands = [
        "python: run",
        "python: debug",
        "debug: start",
        "test: run",
        "python: lint"
    ]
    
    for cmd in python_commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:20} → {result}")
    
    # Test file operations
    print("\n7️⃣  File Operations:")
    file_commands = [
        "file: open",
        "create new file",
        "delete file",
        "rename file",
        "move file to folder"
    ]
    
    for cmd in file_commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:25} → {result}")
    
    # Test search operations
    print("\n8️⃣  Search Operations:")
    search_commands = [
        "search in files",
        "find and replace",
        "grep search",
        "locate symbol",
        "search workspace"
    ]
    
    for cmd in search_commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:25} → {result}")
    
    # Test descriptive commands
    print("\n9️⃣  Descriptive Commands:")
    descriptive_commands = [
        "split editor horizontally",
        "create new terminal in panel",
        "toggle full screen mode",
        "open recent files list",
        "show all keyboard shortcuts"
    ]
    
    for cmd in descriptive_commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:35} → {result}")
    
    # Test simple custom commands
    print("\n🔟  Simple Custom Commands:")
    custom_commands = [
        "continue",
        "next",
        "previous",
        "toggle",
        "refresh"
    ]
    
    for cmd in custom_commands:
        result = send_command_to_cursor(cmd)
        print(f"   {cmd:15} → {result}")
    
    print("\n🎉 Custom Cursor command tests completed!")
    print("\n💡 Available Custom Command Types:")
    print("   • Built-in commands (save, find, format)")
    print("   • Internal commands (workbench.action:...)")
    print("   • Extension commands (git:, python:...)")
    print("   • Command palette (>Git: Add)")
    print("   • Git operations (git: add, git: commit)")
    print("   • Python operations (python: run, debug: start)")
    print("   • File operations (file: open, create new file)")
    print("   • Search operations (search in files, grep)")
    print("   • Descriptive commands (split editor horizontally)")
    print("   • Simple commands (continue, next, toggle)")
    
    print("\n🚀 You can now send ANY command to Cursor!")
    print("\n📱 And from Telegram! Examples:")
    print("   • cursor:cmd 'git: add'")
    print("   • cursor:cmd 'python: run'")
    print("   • cursor:cmd 'workbench.action.files.save'")

if __name__ == "__main__":
    main() 