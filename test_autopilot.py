#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the UwU-CLI Autopilot module
"""

from utils.autopilot import get_autopilot, send_notification

def main():
    print("🧪 Testing UwU-CLI Autopilot...")
    
    # Get autopilot instance
    autopilot = get_autopilot()
    
    if not autopilot:
        print("❌ Failed to initialize autopilot")
        return
    
    if not autopilot.enabled:
        print("❌ Autopilot is disabled in configuration")
        return
    
    print(f"✅ Autopilot initialized with adapters: {autopilot.adapters}")
    
    # Test basic notification
    print("\n📤 Sending test notification...")
    success = autopilot.send_notification(
        "🧪 This is a test message from the autopilot!\n\nTime: " + autopilot._get_timestamp(),
        "Autopilot Test"
    )
    
    if success:
        print("✅ Test notification sent successfully!")
    else:
        print("❌ Test notification failed")
    
    # Test specific notification types
    print("\n📤 Testing specific notification types...")
    
    # CLI start notification
    autopilot.notify_cli_start()
    print("✅ CLI start notification sent")
    
    # Command execution notification
    autopilot.notify_command_executed("ls -la", True)
    print("✅ Command success notification sent")
    
    autopilot.notify_command_executed("invalid_command", False)
    print("✅ Command failure notification sent")
    
    # Error notification
    autopilot.notify_error("Test error message", "Test Context")
    print("✅ Error notification sent")
    
    print("\n🎉 All autopilot tests completed!")

if __name__ == "__main__":
    main() 