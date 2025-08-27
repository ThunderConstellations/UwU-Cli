#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test script to demonstrate chat commands
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_chat_commands():
    """Test the chat commands functionality"""
    print("🧪 Testing Chat Commands...")
    
    try:
        from utils.ai_conversation_manager import get_conversation_manager
        manager = get_conversation_manager()
        
        print("✅ AI Conversation Manager loaded")
        print(f"📊 Total conversations: {len(manager.conversations)}")
        
        # List conversations
        print("\n📋 Listing conversations:")
        conversations = manager.list_conversations(limit=10)
        if conversations:
            for conv in conversations:
                print(f"  📝 {conv['title']}")
                print(f"     ID: {conv['id'][:8]}... | Messages: {conv['message_count']}")
                print(f"     Created: {conv['created_at'][:10]}")
                print()
        else:
            print("  No conversations found")
        
        # Show statistics
        print("📊 Statistics:")
        stats = manager.get_statistics()
        print(f"  Total conversations: {stats['total_conversations']}")
        print(f"  Total messages: {stats['total_messages']}")
        print(f"  Storage size: {stats['storage_size_mb']} MB")
        
        print("\n🎉 Chat commands test completed successfully!")
        print("\n💡 You can now use these commands in UwU-CLI:")
        print("   chat:list              - List all conversations")
        print("   chat:open <id>         - Open a conversation")
        print("   chat:search <query>    - Search conversations")
        print("   chat:export <id>       - Export a conversation")
        print("   chat:stats             - Show statistics")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_chat_commands() 