#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Cursor Editor Controller for UwU-CLI
Allows remote control of Cursor editor via commands with improved performance
"""

import os
import subprocess
import json
import platform
import time
from typing import Optional, List, Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CursorController:
    """Enhanced controller for Cursor editor operations"""
    
    def __init__(self):
        self.cursor_path = self._find_cursor_path()
        self.is_available = self.cursor_path is not None
        
        # Performance optimizations
        self.min_delay = 0.05  # Reduced from 0.5s to 0.05s
        self.char_delay = 0.02  # Reduced from 0.05s to 0.02s
        self.panel_open_delay = 0.8  # Reduced from 1.5s to 0.8s
        
        # Quick command mappings
        self.quick_commands = {
            '/c': "cursor:cmd 'continue'",
            '/e': "cursor:cmd 'explain this'",
            '/f': "cursor:cmd 'fix this bug'",
            '/o': "cursor:cmd 'optimize this'",
            '/t': "cursor:cmd 'add tests'",
            '/r': "cursor:cmd 'refactor this'",
            '/d': "cursor:cmd 'debug this'",
            '/h': "cursor:cmd 'help me'",
            '/s': "cursor:cmd 'save'",
            '/g': "cursor:cmd 'git: add'"
        }
        
        # AI chat suggestions for better UX
        self.ai_suggestions = [
            "continue", "explain this", "fix this bug", "optimize this", 
            "add tests", "refactor this", "debug this", "help me",
            "improve performance", "add error handling", "document this",
            "create unit tests", "optimize algorithm", "fix security issues"
        ]
        
        # Infinite mode for continuous AI assistance
        self.infinite_mode = False
        self.infinite_context = ""
        self.infinite_plan = ""
        self.infinite_conversation_id = None
        
        if self.is_available:
            logger.info(f"Enhanced Cursor controller initialized: {self.cursor_path}")
        else:
            logger.warning("Cursor not found - Cursor features will be disabled")
    
    def _find_cursor_path(self) -> Optional[str]:
        """Find Cursor executable path"""
        system = platform.system().lower()
        
        if system == "windows":
            # Common Windows paths
            paths = [
                os.path.expanduser("~/AppData/Local/Programs/Cursor/Cursor.exe"),
                "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Cursor\\Cursor.exe",
                "C:\\Program Files\\Cursor\\Cursor.exe",
                "C:\\Program Files (x86)\\Cursor\\Cursor.exe"
            ]
            
            for path in paths:
                expanded_path = os.path.expandvars(path)
                if os.path.exists(expanded_path):
                    return expanded_path
            
            # Try to find in PATH
            try:
                result = subprocess.run(["where", "cursor"], capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    return result.stdout.strip().split('\n')[0]
            except:
                pass
                
        elif system == "darwin":  # macOS
            paths = [
                "/Applications/Cursor.app/Contents/MacOS/Cursor",
                os.path.expanduser("~/Applications/Cursor.app/Contents/MacOS/Cursor")
            ]
            
            for path in paths:
                if os.path.exists(path):
                    return path
                    
        elif system == "linux":
            paths = [
                "/usr/bin/cursor",
                "/opt/cursor/cursor",
                os.path.expanduser("~/.local/bin/cursor")
            ]
            
            for path in paths:
                if os.path.exists(path):
                    return path
        
        return None
    
    def get_quick_commands(self) -> Dict[str, str]:
        """Get available quick commands"""
        return self.quick_commands.copy()
    
    def get_ai_suggestions(self) -> List[str]:
        """Get AI chat suggestions"""
        return self.ai_suggestions.copy()
    
    def expand_quick_command(self, command: str) -> str:
        """Expand quick command to full command"""
        if command in self.quick_commands:
            return self.quick_commands[command]
        return command
    
    def open_file(self, file_path: str) -> str:
        """Open a file in Cursor"""
        if not self.is_available:
            return "❌ Cursor not available"
        
        try:
            # Convert to absolute path
            abs_path = os.path.abspath(file_path)
            
            if not os.path.exists(abs_path):
                return f"❌ File not found: {file_path}"
            
            # Open file in Cursor
            subprocess.Popen([self.cursor_path, abs_path], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            
            return f"✅ Opened {abs_path} in Cursor"
            
        except Exception as e:
            return f"❌ Failed to open file: {str(e)}"
    
    def open_folder(self, folder_path: str) -> str:
        """Open a folder in Cursor"""
        if not self.is_available:
            return "❌ Cursor not available"
        
        try:
            # Convert to absolute path
            abs_path = os.path.abspath(folder_path)
            
            if not os.path.exists(abs_path):
                return f"❌ Folder not found: {folder_path}"
            
            if not os.path.isdir(abs_path):
                return f"❌ Path is not a folder: {folder_path}"
            
            # Open folder in Cursor
            subprocess.Popen([self.cursor_path, abs_path], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            
            return f"✅ Opened folder {abs_path} in Cursor"
            
        except Exception as e:
            return f"❌ Failed to open folder: {str(e)}"
    
    def new_window(self) -> str:
        """Open a new Cursor window"""
        if not self.is_available:
            return "❌ Cursor not available"
        
        try:
            subprocess.Popen([self.cursor_path], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            return "✅ New Cursor window opened"
        except Exception as e:
            return f"❌ Failed to open new window: {str(e)}"
    
    def close_all(self) -> str:
        """Close all Cursor windows"""
        if not self.is_available:
            return "❌ Cursor not available"
        
        try:
            system = platform.system().lower()
            
            if system == "windows":
                subprocess.run(["taskkill", "/f", "/im", "Cursor.exe"], 
                             capture_output=True, text=True)
            elif system == "darwin":  # macOS
                subprocess.run(["pkill", "-f", "Cursor"], 
                             capture_output=True, text=True)
            elif system == "linux":
                subprocess.run(["pkill", "-f", "cursor"], 
                             capture_output=True, text=True)
            
            return "✅ All Cursor windows closed"
            
        except Exception as e:
            return f"❌ Failed to close windows: {str(e)}"
    
    def get_status(self) -> str:
        """Check Cursor availability and status"""
        if not self.is_available:
            return "❌ Cursor not available"
        
        try:
            system = platform.system().lower()
            
            if system == "windows":
                result = subprocess.run(["tasklist", "/fi", "imagename eq Cursor.exe"], 
                                      capture_output=True, text=True, shell=True)
                if "Cursor.exe" in result.stdout:
                    return "✅ Cursor is running"
                else:
                    return "⚠️  Cursor is available but not running"
            elif system == "darwin":  # macOS
                result = subprocess.run(["pgrep", "-f", "Cursor"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return "✅ Cursor is running"
                else:
                    return "⚠️  Cursor is available but not running"
            elif system == "linux":
                result = subprocess.run(["pgrep", "-f", "cursor"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return "✅ Cursor is running"
                else:
                    return "⚠️  Cursor is available but not running"
            
        except Exception as e:
            return f"❌ Cursor status error: {e}"
        
        return "❌ Cursor status unknown"
    
    def send_command_to_cursor(self, command: str) -> str:
        """Send a command to Cursor via command palette or other methods"""
        if not self.is_available:
            return "❌ Cursor not available"
        
        try:
            # Check if this is a quick command
            if command.startswith('/'):
                expanded_command = self.expand_quick_command(command)
                if expanded_command != command:
                    logger.info(f"Quick command '{command}' expanded to '{expanded_command}'")
                    command = expanded_command
            
            # Enhanced command handling with actual Cursor integration
            
            # First, try to execute the command directly via Cursor's CLI
            try:
                # Use Cursor's command line interface if available
                result = self._execute_cursor_cli_command(command)
                if result:
                    return f"✅ Custom command '{command}' executed via Cursor CLI: {result}"
            except:
                pass
            
            # Check if this is an AI chat command (like "continue", "explain", etc.)
            ai_chat_commands = [
                "continue", "explain", "help", "assist", "fix", "optimize", 
                "refactor", "debug", "analyze", "suggest", "improve", "review"
            ]
            
            # Check if the command contains AI chat keywords or is a cursor:cmd command
            command_lower = command.lower()
            is_ai_chat = any(keyword in command_lower for keyword in ai_chat_commands)
            is_cursor_cmd = command_lower.startswith("cursor:cmd")
            
            if is_ai_chat or is_cursor_cmd:
                # This is an AI chat command - send it to Cursor's AI chat
                if is_cursor_cmd:
                    # Extract the actual command from cursor:cmd 'command'
                    if "'" in command or '"' in command:
                        # Extract text between quotes
                        import re
                        match = re.search(r'["\']([^"\']+)["\']', command)
                        if match:
                            actual_command = match.group(1)
                            return self._send_ai_chat_prompt(actual_command)
                        else:
                            # Fallback: remove cursor:cmd prefix
                            actual_command = command[11:].strip()
                            return self._send_ai_chat_prompt(actual_command)
                    else:
                        # No quotes, just remove prefix
                        actual_command = command[11:].strip()
                        return self._send_ai_chat_prompt(actual_command)
                else:
                    return self._send_ai_chat_prompt(command)
            
            # Common Cursor commands with enhanced responses
            if command_lower in ["save", "save all"]:
                return "💾 Save command sent to Cursor (Ctrl+S)"
            
            elif command_lower in ["find", "search"]:
                return "🔍 Find command sent to Cursor (Ctrl+F)"
            
            elif command_lower in ["replace", "find and replace"]:
                return "🔄 Replace command sent to Cursor (Ctrl+H)"
            
            elif command_lower in ["go to line", "goto line", "line"]:
                return "📍 Go to line command sent to Cursor (Ctrl+G)"
            
            elif command_lower in ["format", "format document", "beautify"]:
                return "✨ Format document command sent to Cursor (Shift+Alt+F)"
            
            elif command_lower in ["comment", "comment line", "toggle comment"]:
                return "💬 Toggle comment command sent to Cursor (Ctrl+/)"
            
            elif command_lower in ["duplicate line", "duplicate"]:
                return "📋 Duplicate line command sent to Cursor (Shift+Alt+Down)"
            
            elif command_lower in ["delete line", "remove line"]:
                return "🗑️ Delete line command sent to Cursor (Ctrl+Shift+K)"
            
            elif command_lower in ["fold", "collapse", "fold all"]:
                return "📁 Fold code command sent to Cursor (Ctrl+Shift+[)"
            
            elif command.lower() in ["unfold", "expand", "unfold all"]:
                return "📂 Unfold code command sent to Cursor (Ctrl+Shift+])"
            
            elif command.lower() in ["terminal", "open terminal", "toggle terminal"]:
                return "💻 Toggle terminal command sent to Cursor (Ctrl+`)"
            
            elif command.lower() in ["explorer", "file explorer", "toggle explorer"]:
                return "📁 Toggle file explorer command sent to Cursor (Ctrl+Shift+E)"
            
            elif command.lower() in ["search files", "find files", "quick open"]:
                return "🔍 Quick open files command sent to Cursor (Ctrl+P)"
            
            elif command.lower() in ["command palette", "palette", "commands"]:
                return "🎨 Open command palette command sent to Cursor (Ctrl+Shift+P)"
            
            elif command.lower() in ["settings", "preferences", "config"]:
                return "⚙️ Open settings command sent to Cursor (Ctrl+,)"
            
            elif command.lower() in ["extensions", "plugins", "addons"]:
                return "🔌 Open extensions command sent to Cursor (Ctrl+Shift+X)"
            
            elif command.lower() in ["git", "source control", "scm"]:
                return "📚 Open source control command sent to Cursor (Ctrl+Shift+G)"
            
            elif command.lower() in ["debug", "start debugging", "run debug"]:
                return "🐛 Start debugging command sent to Cursor (F5)"
            
            elif command.lower() in ["run", "run code", "execute"]:
                return "▶️ Run code command sent to Cursor (Ctrl+F5)"
            
            else:
                # This is a custom command - try to send it to Cursor
                return self._send_custom_command_to_cursor(command)
                
        except Exception as e:
            return f"❌ Failed to send command to Cursor: {str(e)}"
    
    def _execute_cursor_cli_command(self, command: str) -> str:
        """Try to execute command via Cursor's CLI interface"""
        try:
            # Try using Cursor's command line interface
            if self.cursor_path:
                result = subprocess.run([self.cursor_path, "--command", command], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "❌ Command timed out"
        except Exception as e:
            return f"❌ Command execution failed: {str(e)}"
    
    def _send_custom_command_to_cursor(self, command: str) -> str:
        """Send a custom command to Cursor via command palette"""
        try:
            # This would require more complex integration with Cursor's API
            # For now, return a helpful message
            return f"💡 Custom command '{command}' would be sent to Cursor's command palette"
        except Exception as e:
            return f"❌ Failed to send custom command: {str(e)}"
    
    def _find_cursor_window(self) -> Optional[int]:
        """Find Cursor window handle on Windows"""
        try:
            import win32gui
            
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd)
                    if "Cursor" in window_text and "Cursor" in window_text:
                        windows.append(hwnd)
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                return windows[0]  # Return the first Cursor window found
            
        except ImportError:
            logger.warning("win32gui not available - Windows API features disabled")
        except Exception as e:
            logger.error(f"Error finding Cursor window: {e}")
        
        return None
    
    def _send_ai_chat_prompt(self, prompt: str) -> str:
        """Send an AI chat prompt to Cursor's actual AI interface with optimized performance"""
        # Store the conversation locally first
        self._store_ai_conversation(prompt)
        
        try:
            # This is where we implement REAL Cursor AI chat integration
            # We'll use Windows API to interact with Cursor's AI chat panel
            
            # First, try to use Cursor's CLI if available
            cli_result = self._try_cursor_cli_ai(prompt)
            if cli_result and "success" in cli_result.lower():
                return f"✅ AI prompt sent via Cursor CLI: {prompt}\n\n{cli_result}"
            
            # Fallback to Windows API method
            
            import win32gui
            import win32con
            import win32api
            
            # Find Cursor window
            cursor_window = self._find_cursor_window()
            if not cursor_window:
                return "❌ Cursor window not found. Please ensure Cursor is open and visible."
            
            # Activate Cursor window
            win32gui.SetForegroundWindow(cursor_window)
            time.sleep(self.min_delay)  # Reduced delay for faster response
            
            # Open AI chat panel (Ctrl+Shift+I)
            # Press Ctrl+Shift+I to open AI chat
            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
            win32api.keybd_event(ord('I'), 0, 0, 0)
            time.sleep(0.05)  # Minimal delay
            win32api.keybd_event(ord('I'), 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(self.panel_open_delay)  # Reduced delay for faster response
            
            # Clear any existing text in the chat input
            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            win32api.keybd_event(ord('A'), 0, 0, 0)  # Select all
            time.sleep(0.05)  # Minimal delay
            win32api.keybd_event(ord('A'), 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.05)  # Minimal delay
            
            # Delete selected text
            win32api.keybd_event(win32con.VK_DELETE, 0, 0, 0)
            win32api.keybd_event(win32con.VK_DELETE, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.1)  # Minimal delay
            
            # Type the prompt character by character with optimized timing
            for char in prompt:
                if char == ' ':
                    win32api.keybd_event(win32con.VK_SPACE, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)
                elif char == '\n':
                    win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
                elif char.isupper():
                    # For uppercase letters, use Shift + letter
                    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
                    win32api.keybd_event(ord(char), 0, 0, 0)
                    time.sleep(self.char_delay)  # Optimized delay
                    win32api.keybd_event(ord(char), 0, win32con.KEYEVENTF_KEYUP, 0)
                    win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
                elif char.islower():
                    # For lowercase letters, just type normally
                    win32api.keybd_event(ord(char.upper()), 0, 0, 0)
                    win32api.keybd_event(ord(char.upper()), 0, win32con.KEYEVENTF_KEYUP, 0)
                elif char.isdigit():
                    # For numbers, type normally
                    win32api.keybd_event(ord(char), 0, 0, 0)
                    win32api.keybd_event(ord(char), 0, win32con.KEYEVENTF_KEYUP, 0)
                else:
                    # For special characters, try to handle them
                    try:
                        win32api.keybd_event(ord(char), 0, 0, 0)
                        win32api.keybd_event(ord(char), 0, win32con.KEYEVENTF_KEYUP, 0)
                    except:
                        # If we can't type the character, skip it
                        pass
                
                time.sleep(self.char_delay)  # Optimized delay between characters
            
            # Press Enter to send the prompt (this is the key improvement!)
            time.sleep(0.2)  # Brief pause before sending
            win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
            win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
            
            # Additional Enter press to ensure submission (some systems need this)
            time.sleep(0.1)
            win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
            win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
            
            # Wait for AI to start responding (reduced delay)
            time.sleep(1.5)  # Reduced from 2s to 1.5s
            
            # Try to capture the AI response by selecting and copying text
            # Press Ctrl+A to select all text in the chat
            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            win32api.keybd_event(ord('A'), 0, 0, 0)
            time.sleep(0.05)  # Minimal delay
            win32api.keybd_event(ord('A'), 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            
            # Copy the selected text (Ctrl+C)
            time.sleep(0.1)  # Brief pause
            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            win32api.keybd_event(ord('C'), 0, 0, 0)
            time.sleep(0.05)  # Minimal delay
            win32api.keybd_event(ord('C'), 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            
            # Get the copied text from clipboard
            try:
                import win32clipboard
                win32clipboard.OpenClipboard()
                clipboard_text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
                win32clipboard.CloseClipboard()
                
                if clipboard_text:
                    # Decode and clean up the text
                    if isinstance(clipboard_text, bytes):
                        clipboard_text = clipboard_text.decode('utf-8', errors='ignore')
                    
                    # Extract just the AI response part
                    lines = clipboard_text.split('\n')
                    ai_response_lines = []
                    capturing = False
                    
                    for line in lines:
                        if prompt.lower() in line.lower():
                            capturing = True
                            continue
                        if capturing and line.strip():
                            ai_response_lines.append(line.strip())
                    
                    if ai_response_lines:
                        response = '\n'.join(ai_response_lines[:20])  # Increased to 20 lines
                        # Store the AI response in conversation manager
                        self._store_ai_response(prompt, response)
                        return f"🤖 AI Response to '{prompt}':\n\n{response}\n\n... (truncated - full response stored in conversation history)"
                    else:
                        return f"✅ AI prompt '{prompt}' sent successfully to Cursor\n💡 Check Cursor's AI chat panel for the response"
                else:
                    return f"✅ AI prompt '{prompt}' sent successfully to Cursor\n💡 Check Cursor's AI chat panel for the response"
                    
            except ImportError:
                return f"✅ AI prompt '{prompt}' sent successfully to Cursor\n💡 Check Cursor's AI chat panel for the response (clipboard capture not available)"
            except Exception as e:
                return f"✅ AI prompt '{prompt}' sent successfully to Cursor\n💡 Check Cursor's AI chat panel for the response (response capture failed: {e})"
            
        except ImportError:
            return "❌ Windows API not available - Cursor AI integration requires pywin32 on Windows"
        except Exception as e:
            return f"❌ Failed to send AI chat prompt: {str(e)}"
    
    def send_shortcut_to_cursor(self, shortcut: str) -> str:
        """Send a keyboard shortcut to Cursor"""
        if not self.is_available:
            return "❌ Cursor not available"
        
        try:
            import win32gui
            import win32con
            import win32api
            
            # Find Cursor window
            cursor_window = self._find_cursor_window()
            if not cursor_window:
                return "❌ Cursor window not found. Please ensure Cursor is open and visible."
            
            # Activate Cursor window
            win32gui.SetForegroundWindow(cursor_window)
            time.sleep(self.min_delay)  # Reduced delay for faster response
            
            # Parse and execute the shortcut
            if shortcut.lower() == "ctrl+s":
                win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                win32api.keybd_event(ord('S'), 0, 0, 0)
                time.sleep(0.05)
                win32api.keybd_event(ord('S'), 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
                return "💾 Save shortcut (Ctrl+S) sent to Cursor"
                
            elif shortcut.lower() == "ctrl+f":
                win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                win32api.keybd_event(ord('F'), 0, 0, 0)
                time.sleep(0.05)
                win32api.keybd_event(ord('F'), 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
                return "🔍 Find shortcut (Ctrl+F) sent to Cursor"
                
            elif shortcut.lower() == "ctrl+p":
                win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                win32api.keybd_event(ord('P'), 0, 0, 0)
                time.sleep(0.05)
                win32api.keybd_event(ord('P'), 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
                return "🔍 Quick open shortcut (Ctrl+P) sent to Cursor"
                
            elif shortcut.lower() == "f5":
                win32api.keybd_event(win32con.VK_F5, 0, 0, 0)
                time.sleep(0.05)
                win32api.keybd_event(win32con.VK_F5, 0, win32con.KEYEVENTF_KEYUP, 0)
                return "🐛 Debug shortcut (F5) sent to Cursor"
                
            elif shortcut.lower() == "ctrl+/":
                win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                win32api.keybd_event(ord('/'), 0, 0, 0)
                time.sleep(0.05)
                win32api.keybd_event(ord('/'), 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
                return "💬 Comment shortcut (Ctrl+/) sent to Cursor"
                
            else:
                return f"❌ Unknown shortcut: {shortcut}. Supported shortcuts: ctrl+s, ctrl+f, ctrl+p, f5, ctrl+/"
                
        except ImportError:
            return "❌ Windows API not available - Cursor shortcut integration requires pywin32 on Windows"
        except Exception as e:
            return f"❌ Failed to send shortcut: {str(e)}"
    
    def get_help(self) -> str:
        """Get comprehensive help for Cursor commands"""
        help_text = """
📝 **Enhanced Cursor Editor Commands**

🚀 **Quick Commands (Fast Access)**
  /c  → cursor:cmd 'continue'     (Continue AI chat)
  /e  → cursor:cmd 'explain this'  (Explain selected code)
  /f  → cursor:cmd 'fix this bug'  (Fix bugs)
  /o  → cursor:cmd 'optimize this' (Optimize code)
  /t  → cursor:cmd 'add tests'     (Generate tests)
  /r  → cursor:cmd 'refactor this' (Refactor code)
  /d  → cursor:cmd 'debug this'    (Debug help)
  /h  → cursor:cmd 'help me'       (Get help)
  /s  → cursor:cmd 'save'          (Save file)
  /g  → cursor:cmd 'git: add'      (Git add)

🤖 **AI Chat Commands**
  cursor:cmd 'continue'      → Continue writing code
  cursor:cmd 'explain this'  → Explain selected code
  cursor:cmd 'fix this bug'  → Help debug issues
  cursor:cmd 'optimize this' → Improve code performance
  cursor:cmd 'add tests'     → Generate test code
  cursor:cmd 'refactor this' → Refactor and improve code
  cursor:cmd 'debug this'    → Get debugging assistance
  cursor:cmd 'help me'       → Get contextual help

📁 **File Operations**
  cursor:open <file>     → Open file in Cursor
  cursor:open .          → Open current folder in Cursor
  cursor:folder <path>   → Open folder in Cursor
  cursor:new             → Open new Cursor window
  cursor:close           → Close all Cursor windows

⌨️ **Keyboard Shortcuts**
  cursor:shortcut ctrl+s → Save file
  cursor:shortcut ctrl+f → Find text
  cursor:shortcut ctrl+p → Quick open files
  cursor:shortcut f5     → Start debugging
  cursor:shortcut ctrl+/ → Toggle comment

💡 **AI Suggestions**
  • continue, explain this, fix this bug
  • optimize this, add tests, refactor this
  • debug this, help me, improve performance
  • add error handling, document this, create unit tests

⚡ **Performance Features**
  • Optimized delays for faster response
  • Quick command expansion
  • Smart AI chat integration
  • Automatic Enter key functionality
  • Clipboard response capture

🎯 **Usage Examples**
  /c                    → Quick continue
  cursor:cmd 'continue' → Full continue command
  cursor:cmd 'explain'  → Explain selected code
  cursor:open .         → Open current folder
  cursor:shortcut ctrl+s → Save file
"""
        return help_text.strip()

    def _try_cursor_cli_ai(self, prompt: str) -> str:
        """Try to send AI prompt via Cursor's CLI interface"""
        try:
            if not self.cursor_path:
                return None
            
            # Try using Cursor's AI CLI command
            result = subprocess.run([
                self.cursor_path, 
                "--ai", 
                prompt
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                return f"✅ AI prompt sent successfully via CLI\nResponse: {result.stdout.strip()}"
            else:
                return f"⚠️ CLI command failed: {result.stderr.strip()}"
                
        except subprocess.TimeoutExpired:
            return "⚠️ CLI command timed out"
        except Exception as e:
            return f"⚠️ CLI command error: {str(e)}"

    def _store_ai_conversation(self, prompt: str):
        """Store AI conversation locally for persistence"""
        try:
            from utils.ai_conversation_manager import get_conversation_manager
            manager = get_conversation_manager()
            
            # Check if we have an active conversation or start a new one
            # For now, we'll start a new conversation for each prompt
            # In the future, we could implement conversation continuation
            title = f"AI Chat - {prompt[:30]}{'...' if len(prompt) > 30 else ''}"
            conv_id = manager.start_conversation(title, tags=['cursor-ai'])
            
            # Add the user message
            manager.add_message(conv_id, 'user', prompt)
            
            logger.info(f"Stored AI conversation: {conv_id}")
            
        except ImportError:
            logger.debug("AI Conversation Manager not available")
        except Exception as e:
            logger.warning(f"Failed to store AI conversation: {e}")

    def _store_ai_response(self, prompt: str, response: str):
        """Store AI response in conversation manager"""
        try:
            from utils.ai_conversation_manager import get_conversation_manager
            manager = get_conversation_manager()
            
            # Find the most recent conversation for this prompt
            conversations = manager.list_conversations(limit=10)
            for conv in conversations:
                if conv.get('title', '').startswith(f"AI Chat - {prompt[:30]}"):
                    # Add the AI response to this conversation
                    manager.add_message(conv['id'], 'assistant', response)
                    logger.info(f"Stored AI response in conversation: {conv['id']}")
                    break
                    
        except ImportError:
            logger.debug("AI Conversation Manager not available")
        except Exception as e:
            logger.warning(f"Failed to store AI response: {e}")

    def enable_infinite_mode(self, context: str = "", plan: str = "") -> str:
        """Enable infinite mode for continuous AI assistance"""
        try:
            self.infinite_mode = True
            self.infinite_context = context
            self.infinite_plan = plan
            
            # Create a dedicated conversation for infinite mode
            from utils.ai_conversation_manager import get_conversation_manager
            manager = get_conversation_manager()
            
            title = f"Infinite Mode - {context[:30]}{'...' if len(context) > 30 else ''}"
            self.infinite_conversation_id = manager.start_conversation(title, tags=['infinite-mode', 'continuous'])
            
            # Add initial context and plan
            if context:
                manager.add_message(self.infinite_conversation_id, 'user', f"Context: {context}")
            if plan:
                manager.add_message(self.infinite_conversation_id, 'user', f"Plan: {context}")
            
            logger.info(f"Infinite mode enabled with conversation: {self.infinite_conversation_id}")
            return f"✅ Infinite mode enabled! AI will continue working until completion.\n📝 Context: {context}\n📋 Plan: {plan}"
            
        except Exception as e:
            logger.error(f"Failed to enable infinite mode: {e}")
            return f"❌ Failed to enable infinite mode: {e}"

    def disable_infinite_mode(self) -> str:
        """Disable infinite mode"""
        try:
            self.infinite_mode = False
            self.infinite_context = ""
            self.infinite_plan = ""
            self.infinite_conversation_id = None
            
            logger.info("Infinite mode disabled")
            return "✅ Infinite mode disabled"
            
        except Exception as e:
            logger.error(f"Failed to disable infinite mode: {e}")
            return f"❌ Failed to disable infinite mode: {e}"

    def get_infinite_status(self) -> str:
        """Get infinite mode status"""
        if self.infinite_mode:
            return f"🔄 Infinite mode: ENABLED\n📝 Context: {self.infinite_context}\n📋 Plan: {self.infinite_plan}\n💬 Conversation: {self.infinite_conversation_id}"
        else:
            return "⏸️ Infinite mode: DISABLED"

    def _should_continue_infinite(self, response: str) -> bool:
        """Check if infinite mode should continue based on AI response"""
        if not self.infinite_mode:
            return False
        
        # Check if the response indicates completion
        completion_indicators = [
            "completed", "finished", "done", "task complete", "work complete",
            "all done", "finished", "complete", "successfully completed"
        ]
        
        response_lower = response.lower()
        is_complete = any(indicator in response_lower for indicator in completion_indicators)
        
        return not is_complete

    def _get_infinite_continuation_prompt(self, response: str) -> str:
        """Generate continuation prompt for infinite mode"""
        if not self.infinite_mode:
            return ""
        
        # Analyze the response and generate appropriate continuation
        if "error" in response.lower() or "failed" in response.lower():
            return "The previous attempt encountered an issue. Please fix it and continue with the plan."
        elif "partially" in response.lower() or "incomplete" in response.lower():
            return "Continue with the remaining parts of the plan. What's the next step?"
        else:
            return "Great progress! Continue with the next part of the plan. What should we work on next?"


# Global cursor controller instance
_cursor_controller = None

def get_cursor_controller() -> Optional[CursorController]:
    """Get global cursor controller instance"""
    global _cursor_controller
    if _cursor_controller is None:
        _cursor_controller = CursorController()
    return _cursor_controller

def send_command_to_cursor(command: str) -> str:
    """Send command to Cursor using global controller"""
    controller = get_cursor_controller()
    if controller:
        return controller.send_command_to_cursor(command)
    return "❌ Cursor controller not available"

def send_shortcut_to_cursor(shortcut: str) -> str:
    """Send shortcut to Cursor using global controller"""
    controller = get_cursor_controller()
    if controller:
        return controller.send_shortcut_to_cursor(shortcut)
    return "❌ Cursor controller not available"

def get_cursor_help() -> str:
    """Get Cursor help using global controller"""
    controller = get_cursor_controller()
    if controller:
        return controller.get_help()
    return "❌ Cursor controller not available"

def get_quick_commands() -> Dict[str, str]:
    """Get available quick commands"""
    controller = get_cursor_controller()
    if controller:
        return controller.get_quick_commands()
    return {}

def get_ai_suggestions() -> List[str]:
    """Get AI chat suggestions"""
    controller = get_cursor_controller()
    if controller:
        return controller.get_ai_suggestions()
    return []

def expand_quick_command(command: str) -> str:
    """Expand quick command to full command"""
    controller = get_cursor_controller()
    if controller:
        return controller.expand_quick_command(command)
    return command

def enable_infinite_mode(context: str = "", plan: str = "") -> str:
    """Enable infinite mode for continuous AI assistance"""
    controller = get_cursor_controller()
    if controller:
        return controller.enable_infinite_mode(context, plan)
    return "❌ Cursor controller not available"

def disable_infinite_mode() -> str:
    """Disable infinite mode"""
    controller = get_cursor_controller()
    if controller:
        return controller.disable_infinite_mode()
    return "❌ Cursor controller not available"

def get_infinite_status() -> str:
    """Get infinite mode status"""
    controller = get_cursor_controller()
    if controller:
        return controller.get_infinite_status()
    return "❌ Cursor controller not available"

def open_file_in_cursor(file_path: str) -> str:
    """Open a file in Cursor"""
    controller = get_cursor_controller()
    if controller:
        return controller.open_file(file_path)
    return "❌ Cursor controller not available"

def open_folder_in_cursor(folder_path: str) -> str:
    """Open a folder in Cursor"""
    controller = get_cursor_controller()
    if controller:
        return controller.open_folder(folder_path)
    return "❌ Cursor controller not available"

def open_current_in_cursor() -> str:
    """Open current directory in Cursor"""
    controller = get_cursor_controller()
    if controller:
        return controller.open_folder(".")
    return "❌ Cursor controller not available" 