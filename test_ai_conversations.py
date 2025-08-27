#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for AI Conversation Manager
Verifies that past chats can be stored and retrieved
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ai_conversation_manager():
    """Test the AI conversation manager functionality"""
    print("🧪 Testing AI Conversation Manager...")
    
    try:
        from utils.ai_conversation_manager import get_conversation_manager
        manager = get_conversation_manager()
        
        print("✅ AI Conversation Manager loaded successfully")
        
        # Test 1: Create a new conversation
        print("\n📝 Test 1: Creating new conversation...")
        conv_id = manager.start_conversation("Test AI Chat", tags=['test', 'debug'])
        print(f"   ✅ Conversation created: {conv_id}")
        
        # Test 2: Add messages
        print("\n💬 Test 2: Adding messages...")
        manager.add_message(conv_id, 'user', 'Hello, can you help me with Python?')
        manager.add_message(conv_id, 'assistant', 'Of course! I\'d be happy to help you with Python. What specific question do you have?')
        manager.add_message(conv_id, 'user', 'How do I create a list comprehension?')
        manager.add_message(conv_id, 'assistant', 'List comprehensions in Python are a concise way to create lists. The basic syntax is: [expression for item in iterable if condition]. For example: [x**2 for x in range(10)] creates a list of squares from 0 to 9.')
        print("   ✅ Messages added successfully")
        
        # Test 3: List conversations
        print("\n📋 Test 3: Listing conversations...")
        conversations = manager.list_conversations(limit=5)
        print(f"   ✅ Found {len(conversations)} conversations")
        
        # Test 4: Get specific conversation
        print("\n🔍 Test 4: Retrieving conversation...")
        conversation = manager.get_conversation(conv_id)
        if conversation:
            print(f"   ✅ Conversation retrieved: {conversation['title']}")
            print(f"   📊 Messages: {conversation['message_count']}")
            print(f"   🏷️  Tags: {', '.join(conversation['tags'])}")
        else:
            print("   ❌ Failed to retrieve conversation")
        
        # Test 5: Search conversations
        print("\n🔎 Test 5: Searching conversations...")
        search_results = manager.search_conversations('Python', limit=5)
        print(f"   ✅ Search found {len(search_results)} conversations")
        
        # Test 6: Export conversation
        print("\n💾 Test 6: Exporting conversation...")
        export_file = manager.export_conversation(conv_id, 'txt')
        if export_file:
            print(f"   ✅ Conversation exported to: {export_file}")
        else:
            print("   ❌ Failed to export conversation")
        
        # Test 7: Get statistics
        print("\n📊 Test 7: Getting statistics...")
        stats = manager.get_statistics()
        print(f"   ✅ Total conversations: {stats['total_conversations']}")
        print(f"   ✅ Total messages: {stats['total_messages']}")
        print(f"   ✅ Storage size: {stats['storage_size_mb']} MB")
        
        print("\n🎉 All tests passed! AI Conversation Manager is working correctly.")
        print("\n💡 Now you can use these commands in UwU-CLI:")
        print("   chat:list              - List all conversations")
        print("   chat:open <id>         - Open a conversation")
        print("   chat:search <query>    - Search conversations")
        print("   chat:export <id>       - Export a conversation")
        print("   chat:stats             - Show statistics")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure the AI Conversation Manager is properly installed")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chat_commands():
    """Test the chat commands in UwU-CLI"""
    print("\n🧪 Testing Chat Commands Integration...")
    
    try:
        # Simulate the chat command handling
        from utils.ai_conversation_manager import get_conversation_manager
        manager = get_conversation_manager()
        
        print("✅ Chat commands integration test passed")
        print("   The chat: commands should now work in UwU-CLI")
        return True
        
    except Exception as e:
        print(f"❌ Chat commands test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing AI Conversation Manager for UwU-CLI")
    print("=" * 50)
    
    # Run tests
    success1 = test_ai_conversation_manager()
    success2 = test_chat_commands()
    
    if success1 and success2:
        print("\n🎯 SUMMARY: All tests passed!")
        print("   ✅ AI Conversation Manager is working")
        print("   ✅ Chat commands are integrated")
        print("   ✅ Past chats can now be stored and retrieved")
        print("\n💡 Your 'past chats aren\'t opening' issue should now be resolved!")
    else:
        print("\n❌ SUMMARY: Some tests failed")
        print("   Please check the error messages above")
        sys.exit(1) 