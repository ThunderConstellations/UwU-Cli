#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Cursor AI Chat Integration
"""

import time
from utils.cursor_controller import get_cursor_controller

def test_cursor_ai_chat():
    """Test the cursor AI chat integration"""
    print("🧪 Testing Cursor AI Chat Integration...")
    
    # Get cursor controller
    controller = get_cursor_controller()
    if not controller.is_available:
        print("❌ Cursor not available")
        return
    
    print("✅ Cursor controller available")
    
    # Test window finding
    window = controller._find_cursor_window()
    if not window:
        print("❌ Cursor window not found")
        return
    
    print(f"✅ Cursor window found: {window}")
    
    # Test AI chat prompt
    print("\n🤖 Testing AI chat prompt...")
    print("⚠️  Make sure Cursor is open and visible!")
    print("⚠️  This will send 'continue' to Cursor's AI chat")
    
    # Countdown
    for i in range(5, 0, -1):
        print(f"⏰ Starting in {i} seconds...")
        time.sleep(1)
    
    print("🚀 Sending prompt to Cursor AI chat...")
    
    try:
        result = controller._send_ai_chat_prompt("continue")
        print("\n📱 Result:")
        print(result)
        
        if "AI Chat Prompt Sent Successfully" in result:
            print("\n✅ SUCCESS: AI chat prompt sent to Cursor!")
        else:
            print("\n❌ FAILED: AI chat prompt not sent properly")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cursor_ai_chat() 