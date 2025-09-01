#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Telegram Command Control
"""

from utils.telegram_controller import get_telegram_controller, start_telegram_control, stop_telegram_control

def mock_command_executor(command: str) -> str:
    """Mock command executor for testing"""
    print(f"🔧 Executing command: {command}")
    
    # Simulate some command results
    if command.lower() == "ls" or command.lower() == "dir":
        return "📁 Documents\n📁 Downloads\n📁 Pictures\n📄 test.txt\n📄 README.md"
    elif command.lower() == "pwd" or command.lower() == "cd":
        return "/home/user/current/directory"
    elif command.lower() == "date":
        return "2024-12-17 08:45:00"
    elif command.lower() == "whoami":
        return "testuser"
    else:
        return f"Command '{command}' executed successfully (mock result)"

def main():
    print("🎮 Testing Telegram Command Control...")
    
    # Get controller instance
    controller = get_telegram_controller()
    
    if not controller:
        print("❌ Failed to initialize Telegram controller")
        return
    
    print("✅ Telegram controller initialized")
    
    # Test starting the controller
    print("\n🚀 Starting Telegram command control...")
    if start_telegram_control(mock_command_executor):
        print("✅ Telegram command control started successfully!")
        print("📱 Now you can send commands to your bot:")
        print("   • Send 'ls' to list files")
        print("   • Send 'pwd' to show current directory")
        print("   • Send 'date' to show current time")
        print("   • Send any other command to test")
        print("\n💡 Bot commands:")
        print("   • /start - Show help")
        print("   • /status - Check status")
        print("   • /help - Show help")
        
        print("\n⏳ Controller is running... Press Ctrl+C to stop")
        
        try:
            # Keep running
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping controller...")
            stop_telegram_control()
            print("✅ Controller stopped")
    
    else:
        print("❌ Failed to start Telegram command control")
        print("💡 Make sure your .autopilot.json is configured correctly")

if __name__ == "__main__":
    main() 