#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Cursor Editor Control
"""

from utils.cursor_controller import get_cursor_controller, open_file_in_cursor, open_folder_in_cursor, open_current_in_cursor

def main():
    print("📝 Testing Cursor Editor Control...")
    
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
    
    print("\n🧪 Testing Cursor Features:")
    
    # Test opening current folder
    print("\n1️⃣  Opening current folder in Cursor...")
    result = open_current_in_cursor()
    print(f"   Result: {result}")
    
    # Test opening a specific file
    print("\n2️⃣  Opening README.md in Cursor...")
    result = open_file_in_cursor("README.md")
    print(f"   Result: {result}")
    
    # Test opening a folder
    print("\n3️⃣  Opening utils folder in Cursor...")
    result = open_folder_in_cursor("utils")
    print(f"   Result: {result}")
    
    # Test new window
    print("\n4️⃣  Opening new Cursor window...")
    result = controller.new_window()
    print(f"   Result: {result}")
    
    print("\n🎉 Cursor control tests completed!")
    print("\n💡 Available Cursor Commands in UwU-CLI:")
    print("   • cursor:open <file>     - Open file in Cursor")
    print("   • cursor:open .          - Open current folder in Cursor")
    print("   • cursor:folder <path>   - Open folder in Cursor")
    print("   • cursor:new             - Open new Cursor window")
    print("   • cursor:close           - Close all Cursor windows")
    print("   • cursor:status          - Check Cursor availability")
    
    print("\n🚀 You can now use these commands in UwU-CLI!")

if __name__ == "__main__":
    main() 