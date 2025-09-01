#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Conversation Manager for UwU-CLI
Stores and retrieves AI chat conversations locally for persistent access
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import uuid

logger = logging.getLogger(__name__)


class AIConversationManager:
    """Manages AI conversation storage and retrieval"""
    
    def __init__(self, data_dir: str = "tmp"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Conversation storage files
        self.conversations_file = self.data_dir / "ai_conversations.json"
        self.conversation_index_file = self.data_dir / "conversation_index.json"
        
        # Load existing conversations
        self.conversations = self._load_conversations()
        self.conversation_index = self._load_conversation_index()
        
        # Settings
        self.max_conversations = 100  # Keep last 100 conversations
        self.max_messages_per_conversation = 50  # Keep last 50 messages per conversation
        
        logger.info("AI Conversation Manager initialized")
    
    def _load_conversations(self) -> Dict[str, Dict[str, Any]]:
        """Load existing conversations from storage"""
        try:
            if self.conversations_file.exists():
                with open(self.conversations_file, 'r', encoding='utf-8') as f:
                    conversations = json.load(f)
                    logger.info(f"Loaded {len(conversations)} AI conversations")
                    return conversations
        except Exception as e:
            logger.warning(f"Failed to load conversations: {e}")
        
        return {}
    
    def _load_conversation_index(self) -> Dict[str, Any]:
        """Load conversation index for quick searching"""
        try:
            if self.conversation_index_file.exists():
                with open(self.conversation_index_file, 'r', encoding='utf-8') as f:
                    index = json.load(f)
                    logger.info("Conversation index loaded")
                    return index
        except Exception as e:
            logger.warning(f"Failed to load conversation index: {e}")
        
        return {
            'conversation_count': 0,
            'last_updated': datetime.now().isoformat(),
            'tags': {},
            'search_index': {}
        }
    
    def _save_conversations(self):
        """Save conversations to storage"""
        try:
            # Clean up old conversations if we exceed the limit
            if len(self.conversations) > self.max_conversations:
                # Remove oldest conversations
                sorted_conversations = sorted(
                    self.conversations.items(),
                    key=lambda x: x[1].get('last_updated', '1970-01-01T00:00:00')
                )
                conversations_to_remove = len(self.conversations) - self.max_conversations
                for i in range(conversations_to_remove):
                    conv_id = sorted_conversations[i][0]
                    del self.conversations[conv_id]
                
                logger.info(f"Cleaned up {conversations_to_remove} old conversations")
            
            with open(self.conversations_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversations, f, indent=2, default=str)
            
            logger.debug("Conversations saved successfully")
        except Exception as e:
            logger.error(f"Failed to save conversations: {e}")
    
    def _save_conversation_index(self):
        """Save conversation index to storage"""
        try:
            self.conversation_index['last_updated'] = datetime.now().isoformat()
            self.conversation_index['conversation_count'] = len(self.conversations)
            
            with open(self.conversation_index_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_index, f, indent=2, default=str)
            
            logger.debug("Conversation index saved successfully")
        except Exception as e:
            logger.error(f"Failed to save conversation index: {e}")
    
    def start_conversation(self, title: str = None, tags: List[str] = None) -> str:
        """Start a new AI conversation"""
        conversation_id = str(uuid.uuid4())
        
        if not title:
            title = f"AI Chat {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        conversation = {
            'id': conversation_id,
            'title': title,
            'tags': tags or [],
            'messages': [],
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'message_count': 0,
            'total_tokens': 0
        }
        
        self.conversations[conversation_id] = conversation
        
        # Update index
        self._update_conversation_index(conversation_id, conversation)
        
        # Save to storage
        self._save_conversations()
        self._save_conversation_index()
        
        logger.info(f"Started new AI conversation: {title}")
        return conversation_id
    
    def add_message(self, conversation_id: str, role: str, content: str, 
                   tokens: int = 0, metadata: Dict[str, Any] = None) -> bool:
        """Add a message to an existing conversation"""
        if conversation_id not in self.conversations:
            logger.error(f"Conversation {conversation_id} not found")
            return False
        
        conversation = self.conversations[conversation_id]
        
        message = {
            'id': str(uuid.uuid4()),
            'role': role,  # 'user' or 'assistant'
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'tokens': tokens,
            'metadata': metadata or {}
        }
        
        conversation['messages'].append(message)
        conversation['last_updated'] = datetime.now().isoformat()
        conversation['message_count'] = len(conversation['messages'])
        conversation['total_tokens'] += tokens
        
        # Clean up old messages if we exceed the limit
        if len(conversation['messages']) > self.max_messages_per_conversation:
            messages_to_remove = len(conversation['messages']) - self.max_messages_per_conversation
            conversation['messages'] = conversation['messages'][-self.max_messages_per_conversation:]
            logger.debug(f"Cleaned up {messages_to_remove} old messages from conversation {conversation_id}")
        
        # Update index
        self._update_conversation_index(conversation_id, conversation)
        
        # Save to storage
        self._save_conversations()
        self._save_conversation_index()
        
        logger.debug(f"Added message to conversation {conversation_id}")
        return True
    
    def _update_conversation_index(self, conversation_id: str, conversation: Dict[str, Any]):
        """Update the conversation index with new information"""
        # Update tags index
        for tag in conversation.get('tags', []):
            if tag not in self.conversation_index['tags']:
                self.conversation_index['tags'][tag] = []
            if conversation_id not in self.conversation_index['tags'][tag]:
                self.conversation_index['tags'][tag].append(conversation_id)
        
        # Update search index
        search_text = f"{conversation['title']} {' '.join(conversation.get('tags', []))}"
        search_text += ' '.join([msg.get('content', '') for msg in conversation.get('messages', [])])
        
        # Simple word-based indexing
        words = search_text.lower().split()
        for word in words:
            if len(word) > 2:  # Only index words longer than 2 characters
                if word not in self.conversation_index['search_index']:
                    self.conversation_index['search_index'][word] = []
                if conversation_id not in self.conversation_index['search_index'][word]:
                    self.conversation_index['search_index'][word].append(conversation_id)
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific conversation by ID"""
        return self.conversations.get(conversation_id)
    
    def list_conversations(self, limit: int = 20, offset: int = 0, 
                          tag: str = None, search_query: str = None) -> List[Dict[str, Any]]:
        """List conversations with optional filtering"""
        conversations = list(self.conversations.values())
        
        # Filter by tag if specified
        if tag:
            conversations = [c for c in conversations if tag in c.get('tags', [])]
        
        # Filter by search query if specified
        if search_query:
            query_words = search_query.lower().split()
            matching_conversations = []
            
            for conv in conversations:
                search_text = f"{conv.get('title', '')} {' '.join(conv.get('tags', []))}"
                search_text += ' '.join([msg.get('content', '') for msg in conv.get('messages', [])])
                search_text = search_text.lower()
                
                if any(word in search_text for word in query_words):
                    matching_conversations.append(conv)
            
            conversations = matching_conversations
        
        # Sort by last updated (newest first)
        conversations.sort(key=lambda x: x.get('last_updated', '1970-01-01T00:00:00'), reverse=True)
        
        # Apply pagination
        start = offset
        end = start + limit
        return conversations[start:end]
    
    def search_conversations(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search conversations by content"""
        return self.list_conversations(limit=limit, search_query=query)
    
    def get_conversation_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """Get conversation by title (exact match)"""
        for conv in self.conversations.values():
            if conv.get('title') == title:
                return conv
        return None
    
    def update_conversation_title(self, conversation_id: str, new_title: str) -> bool:
        """Update the title of a conversation"""
        if conversation_id not in self.conversations:
            return False
        
        self.conversations[conversation_id]['title'] = new_title
        self.conversations[conversation_id]['last_updated'] = datetime.now().isoformat()
        
        self._save_conversations()
        logger.info(f"Updated conversation title: {new_title}")
        return True
    
    def add_tags_to_conversation(self, conversation_id: str, tags: List[str]) -> bool:
        """Add tags to a conversation"""
        if conversation_id not in self.conversations:
            return False
        
        conversation = self.conversations[conversation_id]
        existing_tags = set(conversation.get('tags', []))
        new_tags = set(tags)
        
        conversation['tags'] = list(existing_tags | new_tags)
        conversation['last_updated'] = datetime.now().isoformat()
        
        # Update index
        self._update_conversation_index(conversation_id, conversation)
        
        self._save_conversations()
        self._save_conversation_index()
        
        logger.info(f"Added tags {tags} to conversation {conversation_id}")
        return True
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        if conversation_id not in self.conversations:
            return False
        
        # Remove from conversations
        del self.conversations[conversation_id]
        
        # Clean up index
        self._cleanup_index_for_conversation(conversation_id)
        
        # Save changes
        self._save_conversations()
        self._save_conversation_index()
        
        logger.info(f"Deleted conversation {conversation_id}")
        return True
    
    def _cleanup_index_for_conversation(self, conversation_id: str):
        """Remove conversation references from index"""
        # Remove from tags
        for tag in list(self.conversation_index['tags'].keys()):
            if conversation_id in self.conversation_index['tags'][tag]:
                self.conversation_index['tags'][tag].remove(conversation_id)
                if not self.conversation_index['tags'][tag]:
                    del self.conversation_index['tags'][tag]
        
        # Remove from search index
        for word in list(self.conversation_index['search_index'].keys()):
            if conversation_id in self.conversation_index['search_index'][word]:
                self.conversation_index['search_index'][word].remove(conversation_id)
                if not self.conversation_index['search_index'][word]:
                    del self.conversation_index['search_index'][word]
    
    def export_conversation(self, conversation_id: str, format: str = 'json') -> Optional[str]:
        """Export a conversation to a file"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return None
        
        try:
            if format.lower() == 'json':
                export_file = self.data_dir / f"conversation_export_{conversation_id[:8]}.json"
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(conversation, f, indent=2, default=str)
                
                logger.info(f"Exported conversation to {export_file}")
                return str(export_file)
            
            elif format.lower() == 'txt':
                export_file = self.data_dir / f"conversation_export_{conversation_id[:8]}.txt"
                with open(export_file, 'w', encoding='utf-8') as f:
                    f.write(f"Conversation: {conversation['title']}\n")
                    f.write(f"Created: {conversation['created_at']}\n")
                    f.write(f"Tags: {', '.join(conversation.get('tags', []))}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for message in conversation.get('messages', []):
                        role = message['role'].upper()
                        timestamp = message['timestamp']
                        content = message['content']
                        f.write(f"[{timestamp}] {role}: {content}\n\n")
                
                logger.info(f"Exported conversation to {export_file}")
                return str(export_file)
            
            else:
                logger.error(f"Unsupported export format: {format}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to export conversation: {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get conversation statistics"""
        total_conversations = len(self.conversations)
        total_messages = sum(conv.get('message_count', 0) for conv in self.conversations.values())
        total_tokens = sum(conv.get('total_tokens', 0) for conv in self.conversations.values())
        
        # Most used tags
        tag_counts = {}
        for conv in self.conversations.values():
            for tag in conv.get('tags', []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        most_used_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Recent activity
        recent_conversations = sorted(
            self.conversations.values(),
            key=lambda x: x.get('last_updated', '1970-01-01T00:00:00'),
            reverse=True
        )[:5]
        
        return {
            'total_conversations': total_conversations,
            'total_messages': total_messages,
            'total_tokens': total_tokens,
            'most_used_tags': most_used_tags,
            'recent_conversations': [
                {
                    'id': conv['id'],
                    'title': conv['title'],
                    'last_updated': conv['last_updated'],
                    'message_count': conv.get('message_count', 0)
                }
                for conv in recent_conversations
            ],
            'storage_size_mb': self._get_storage_size()
        }
    
    def _get_storage_size(self) -> float:
        """Get the size of conversation storage in MB"""
        try:
            if self.conversations_file.exists():
                size_bytes = self.conversations_file.stat().st_size
                return round(size_bytes / (1024 * 1024), 2)
        except:
            pass
        return 0.0


# Global conversation manager instance
_conversation_manager = None


def get_conversation_manager() -> AIConversationManager:
    """Get global conversation manager instance"""
    global _conversation_manager
    if _conversation_manager is None:
        _conversation_manager = AIConversationManager()
    return _conversation_manager 