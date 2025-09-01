#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
State Manager for UwU-CLI
Implements session persistence, command history tracking, and context maintenance
"""

import os
import json
import pickle
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import time

logger = logging.getLogger(__name__)


class StateManager:
    """Manages UwU-CLI state including sessions, history, and context"""
    
    def __init__(self, data_dir: str = "tmp"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # State files
        self.session_file = self.data_dir / "session.json"
        self.history_file = self.data_dir / "command_history.json"
        self.context_file = self.data_dir / "context.json"
        self.preferences_file = self.data_dir / "preferences.json"
        
        # Session management - Define these BEFORE loading state
        self.session_timeout = timedelta(hours=24)  # 24 hour timeout
        self.max_history_size = 1000  # Max commands to remember
        
        # Current state - Load AFTER defining session_timeout
        self.current_session = self._load_session()
        self.command_history = self._load_history()
        self.context = self._load_context()
        self.preferences = self._load_preferences()
        
        logger.info("State manager initialized")
    
    def _load_session(self) -> Dict[str, Any]:
        """Load current session data"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    
                # Check if session is still valid
                last_activity = datetime.fromisoformat(session_data.get('last_activity', '1970-01-01T00:00:00'))
                if datetime.now() - last_activity < self.session_timeout:
                    logger.info("Session loaded successfully")
                    return session_data
                else:
                    logger.info("Session expired, creating new one")
            
        except Exception as e:
            logger.warning(f"Failed to load session: {e}")
        
        # Create new session
        return self._create_new_session()
    
    def _create_new_session(self) -> Dict[str, Any]:
        """Create a new session"""
        session = {
            'session_id': self._generate_session_id(),
            'start_time': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat(),
            'working_directory': os.getcwd(),
            'user_agent': 'UwU-CLI/1.0',
            'telegram_chat_id': None,
            'cursor_integration': False,
            'security_level': 'high',
            'commands_executed': 0,
            'errors_encountered': 0
        }
        
        self._save_session(session)
        logger.info(f"New session created: {session['session_id']}")
        return session
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID"""
        import uuid
        return str(uuid.uuid4())
    
    def _save_session(self, session: Dict[str, Any]):
        """Save session data to file"""
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
    
    def load_session(self):
        """Load session data from storage"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    self.session = session_data.get('session', {})
                    self.last_activity = session_data.get('last_activity', time.time())
                    print("📊 Session loaded successfully")
            else:
                print("📊 No existing session found, starting fresh")
        except Exception as e:
            print(f"⚠️  Failed to load session: {e}")
            self.session = {}
            self.last_activity = time.time()
    
    def save_session(self):
        """Save session data to storage"""
        try:
            self.last_activity = time.time()
            session_data = {
                'session': self.session,
                'last_activity': self.last_activity
            }
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            print("📊 Session saved successfully")
        except Exception as e:
            print(f"⚠️  Failed to save session: {e}")
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load command history"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    logger.info(f"Loaded {len(history)} command history entries")
                    return history
        except Exception as e:
            logger.warning(f"Failed to load command history: {e}")
        
        return []
    
    def _save_history(self):
        """Save command history to file"""
        try:
            # Keep only recent history
            if len(self.command_history) > self.max_history_size:
                self.command_history = self.command_history[-self.max_history_size:]
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.command_history, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save command history: {e}")
    
    def _load_context(self) -> Dict[str, Any]:
        """Load context data"""
        try:
            if self.context_file.exists():
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    context = json.load(f)
                    logger.info("Context loaded successfully")
                    return context
        except Exception as e:
            logger.warning(f"Failed to load context: {e}")
        
        return {
            'current_theme': 'default',
            'last_working_directory': os.getcwd(),
            'favorite_commands': [],
            'recent_files': [],
            'git_status': {},
            'cursor_state': 'unknown'
        }
    
    def _save_context(self):
        """Save context data to file"""
        try:
            with open(self.context_file, 'w', encoding='utf-8') as f:
                json.dump(self.context, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save context: {e}")
    
    def _load_preferences(self) -> Dict[str, Any]:
        """Load user preferences"""
        try:
            if self.preferences_file.exists():
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    prefs = json.load(f)
                    logger.info("Preferences loaded successfully")
                    return prefs
        except Exception as e:
            logger.warning(f"Failed to load preferences: {e}")
        
        return {
            'auto_save': True,
            'history_size': 1000,
            'session_timeout_hours': 24,
            'security_level': 'high',
            'telegram_notifications': True,
            'cursor_integration': True,
            'theme': 'default',
            'language': 'en'
        }
    
    def _save_preferences(self):
        """Save user preferences to file"""
        try:
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save preferences: {e}")
    
    def update_session_activity(self):
        """Update session activity timestamp"""
        self.current_session['last_activity'] = datetime.now().isoformat()
        self.current_session['commands_executed'] += 1
        self._save_session(self.current_session)
    
    def add_command_to_history(self, command: str, success: bool, 
                             output: str = "", error: str = "", 
                             execution_time: float = 0.0):
        """Add command to history"""
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'success': success,
            'output_length': len(output),
            'error': error,
            'execution_time': execution_time,
            'working_directory': os.getcwd(),
            'session_id': self.current_session['session_id']
        }
        
        self.command_history.append(history_entry)
        self._save_history()
        
        # Update session stats
        if not success:
            self.current_session['errors_encountered'] += 1
        self.update_session_activity()
    
    def get_command_history(self, limit: int = 50, 
                          filter_success: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get command history with optional filtering"""
        history = self.command_history
        
        if filter_success is not None:
            history = [h for h in history if h['success'] == filter_success]
        
        return history[-limit:] if limit > 0 else history
    
    def search_command_history(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search command history by query"""
        results = []
        query_lower = query.lower()
        
        for entry in reversed(self.command_history):
            if query_lower in entry['command'].lower():
                results.append(entry)
                if len(results) >= limit:
                    break
        
        return results
    
    def update_context(self, key: str, value: Any):
        """Update context data"""
        self.context[key] = value
        self._save_context()
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context value"""
        return self.context.get(key, default)
    
    def update_preferences(self, key: str, value: Any):
        """Update user preferences"""
        self.preferences[key] = value
        self._save_preferences()
    
    def get_preferences(self, key: str, default: Any = None) -> Any:
        """Get preference value"""
        return self.preferences.get(key, default)
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get current session information"""
        return {
            'session_id': self.current_session['session_id'],
            'start_time': self.current_session['start_time'],
            'last_activity': self.current_session['last_activity'],
            'commands_executed': self.current_session['commands_executed'],
            'errors_encountered': self.current_session['errors_encountered'],
            'working_directory': os.getcwd(),
            'uptime': self._get_uptime(),
            'history_size': len(self.command_history)
        }
    
    def _get_uptime(self) -> str:
        """Get session uptime as human-readable string"""
        try:
            start_time = datetime.fromisoformat(self.current_session['start_time'])
            uptime = datetime.now() - start_time
            
            if uptime.days > 0:
                return f"{uptime.days}d {uptime.seconds // 3600}h"
            elif uptime.seconds > 3600:
                hours = uptime.seconds // 3600
                minutes = (uptime.seconds % 3600) // 60
                return f"{hours}h {minutes}m"
            elif uptime.seconds > 60:
                minutes = uptime.seconds // 60
                return f"{minutes}m"
            else:
                return f"{uptime.seconds}s"
        except:
            return "Unknown"
    
    def export_session_data(self, filepath: str):
        """Export session data to file"""
        try:
            export_data = {
                'export_time': datetime.now().isoformat(),
                'session': self.current_session,
                'context': self.context,
                'preferences': self.preferences,
                'history_sample': self.command_history[-100:]  # Last 100 commands
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Session data exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to export session data: {e}")
            return False
    
    def clear_history(self):
        """Clear command history"""
        self.command_history = []
        self._save_history()
        logger.info("Command history cleared")
    
    def reset_session(self):
        """Reset current session"""
        self.current_session = self._create_new_session()
        logger.info("Session reset")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get usage statistics"""
        total_commands = len(self.command_history)
        successful_commands = len([h for h in self.command_history if h['success']])
        failed_commands = total_commands - successful_commands
        
        # Most used commands
        command_counts = {}
        for entry in self.command_history:
            cmd = entry['command'].split()[0]  # First word of command
            command_counts[cmd] = command_counts.get(cmd, 0) + 1
        
        most_used = sorted(command_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'total_commands': total_commands,
            'successful_commands': successful_commands,
            'failed_commands': failed_commands,
            'success_rate': (successful_commands / total_commands * 100) if total_commands > 0 else 0,
            'most_used_commands': most_used,
            'average_execution_time': sum(h.get('execution_time', 0) for h in self.command_history) / total_commands if total_commands > 0 else 0,
            'session_uptime': self._get_uptime()
        }


# Global state manager instance
_state_manager = None


def get_state_manager() -> StateManager:
    """Get global state manager instance"""
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager 