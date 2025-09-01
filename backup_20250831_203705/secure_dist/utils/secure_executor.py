#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Secure Command Executor
Provides secure command execution with whitelisting, input validation, and output filtering
"""

import re
import os
import subprocess
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


class SecureExecutor:
    """Secure command executor with comprehensive security measures"""
    
    def __init__(self):
        # Command whitelisting by category
        self.ALLOWED_COMMANDS = {
            'file_ops': [
                'dir', 'ls', 'cd', 'pwd', 'type', 'copy', 'move', 'del', 'md', 'rd'
            ],
            'git_ops': [
                'git status', 'git log', 'git diff', 'git add', 'git commit', 
                'git push', 'git pull', 'git branch', 'git checkout'
            ],
            'build_ops': [
                'npm install', 'npm run', 'python -m pip install', 'python setup.py',
                'mvn install', 'gradle build', 'cargo build'
            ],
            'safe_ops': [
                'echo', 'whoami', 'date', 'time', 'ver', 'systeminfo'
            ],
            'python_ops': [
                'python', 'python -c', 'python -m', 'pip', 'pip install'
            ],
            'node_ops': [
                'node', 'npm', 'npx', 'yarn'
            ]
        }
        
        # Restricted paths that should never be accessed
        self.RESTRICTED_PATHS = [
            '/etc/passwd', '/etc/shadow', '/var/log', '/proc',
            'C:\\Windows\\System32', 'C:\\Users\\Administrator',
            'C:\\Program Files', 'C:\\Program Files (x86)'
        ]
        
        # Sensitive data patterns to mask in output
        self.SENSITIVE_PATTERNS = [
            # API keys and tokens
            (r'api_key\\s*=\\s*[\'"][^\'"]+[\'"]', '
            (r'token\\s*=\\s*[\'"][^\'"]+[\'"]', '
            (r'secret\\s*=\\s*[\'"][^\'"]+[\'"]', '
            (r'password\\s*=\\s*[\'"][^\'"]+[\'"]', 'password = "***MASKED***"'),
            (r'key\\s*=\\s*[\'"][^\'"]+[\'"]', 'key = "***MASKED***"'),
            
            # File paths that might contain sensitive info
            (r'C:\\\\Users\\\\[^\\\\]+\\\\AppData\\\\Local\\\\[^\\\\]+', 'C:\\\\Users\\\\***USER***\\\\AppData\\\\Local\\\\***APP***'),
            (r'/home/[^/]+/\\.', '/home/***USER***/.'),
            
            # Environment variables
            (r'%USERNAME%', '***USERNAME***'),
            (r'%USERPROFILE%', '***USERPROFILE***'),
            (r'%APPDATA%', '***APPDATA***'),
            
            # Git information
            (r'git@github\\.com:[^/]+/[^/]+\.git', 'git@github.com:***ORG***/***REPO***.git'),
            (r'https://github\\.com/[^/]+/[^/]+', 'https://github.com/***ORG***/***REPO***'),
        ]
        
        # Maximum command length
        self.MAX_COMMAND_LENGTH = 1000
        
        # Maximum output length
        self.MAX_OUTPUT_LENGTH = 5000
        
        # Rate limiting (commands per minute)
        self.rate_limit = {}
        self.max_commands_per_minute = 30
    
    def is_command_allowed(self, command: str) -> Tuple[bool, str]:
        """Check if a command is allowed based on whitelist"""
        try:
            # Check command length
            if len(command) > self.MAX_COMMAND_LENGTH:
                return False, f"Command too long (max {self.MAX_COMMAND_LENGTH} characters)"
            
            # Check for dangerous patterns
            dangerous_patterns = [
                r'rm\s+-rf', r'del\s+/s', r'format\s+[c-z]:', r'fdisk',
                r'shutdown', r'reboot', r'taskkill', r'tskill', r'wmic',
                r'powershell\s+-ExecutionPolicy\s+Bypass', r'cmd\s+/c\s+del',
                r'echo\s+.*\s*>\s*[c-z]:\\', r'copy\s+.*\s*[c-z]:\\'
            ]
            
            for pattern in dangerous_patterns:
                if re.search(pattern, command, re.IGNORECASE):
                    return False, f"Command contains dangerous pattern: {pattern}"
            
            # Check for path traversal attempts
            if '..' in command or '~' in command:
                return False, "Path traversal not allowed"
            
            # Check against whitelist
            command_lower = command.lower().strip()
            
            for category, allowed_cmds in self.ALLOWED_COMMANDS.items():
                for allowed_cmd in allowed_cmds:
                    if command_lower.startswith(allowed_cmd.lower()):
                        return True, f"Command allowed (category: {category})"
            
            # Special case: allow commands that are clearly safe
            if command_lower in ['help', 'cls', 'clear', 'exit', 'quit']:
                return True, "Command allowed (safe command)"
            
            return False, "Command not in whitelist"
            
        except Exception as e:
            logger.error(f"Error checking command allowance: {e}")
            return False, f"Error validating command: {str(e)}"
    
    def sanitize_output(self, output: str) -> str:
        """Sanitize output to remove sensitive information"""
        try:
            sanitized = output
            
            # Apply sensitive data patterns
            for pattern, replacement in self.SENSITIVE_PATTERNS:
                sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
            
            # Remove absolute paths that might contain sensitive info
            sanitized = re.sub(r'C:\\Users\\[^\\]+\\', 'C:\\Users\\***USER***\\', sanitized)
            sanitized = re.sub(r'/home/[^/]+/', '/home/***USER***/', sanitized)
            
            # Remove potential API keys (long strings of alphanumeric characters)
            sanitized = re.sub(r'\b[a-zA-Z0-9]{32,}\b', '***LONG_KEY***', sanitized)
            
            # Truncate if too long
            if len(sanitized) > self.MAX_OUTPUT_LENGTH:
                sanitized = sanitized[:self.MAX_OUTPUT_LENGTH] + "\n\n... (truncated for security)"
            
            return sanitized
            
        except Exception as e:
            logger.error(f"Error sanitizing output: {e}")
            return "***OUTPUT_SANITIZATION_ERROR***"
    
    def execute_command(self, command: str, cwd: str = None) -> Tuple[bool, str, str]:
        """Execute a command securely and return (success, output, error_message)"""
        try:
            # Validate command
            is_allowed, reason = self.is_command_allowed(command)
            if not is_allowed:
                return False, "", f"Command rejected: {reason}"
            
            # Check rate limiting
            if not self._check_rate_limit():
                return False, "", "Rate limit exceeded. Please wait before sending more commands."
            
            # Set working directory
            if not cwd:
                cwd = os.getcwd()
            
            # Validate working directory
            if not self._is_safe_directory(cwd):
                return False, "", f"Working directory not safe: {cwd}"
            
            # Execute command
            logger.info(f"Executing secure command: {command} in {cwd}")
            
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=60,  # 60 second timeout
                env=self._get_safe_environment()
            )
            
            # Process output
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            
            # Sanitize output
            sanitized_stdout = self.sanitize_output(stdout)
            sanitized_stderr = self.sanitize_output(stderr)
            
            # Prepare response
            if result.returncode == 0:
                if sanitized_stdout:
                    return True, sanitized_stdout, ""
                else:
                    return True, "Command executed successfully (no output)", ""
            else:
                error_msg = sanitized_stderr if sanitized_stderr else f"Command failed with exit code {result.returncode}"
                return False, "", error_msg
                
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out after 60 seconds"
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return False, "", f"Error executing command: {str(e)}"
    
    def _is_safe_directory(self, directory: str) -> bool:
        """Check if a directory is safe to execute commands in"""
        try:
            abs_path = os.path.abspath(directory)
            
            # Check against restricted paths
            for restricted in self.RESTRICTED_PATHS:
                if restricted.lower() in abs_path.lower():
                    return False
            
            # Check if directory exists and is accessible
            if not os.path.exists(abs_path) or not os.path.isdir(abs_path):
                return False
            
            # Check if it's a development/project directory
            safe_indicators = ['github', 'gitlab', 'project', 'src', 'workspace', 'dev']
            path_lower = abs_path.lower()
            
            # Must contain at least one safe indicator
            has_safe_indicator = any(indicator in path_lower for indicator in safe_indicators)
            
            return has_safe_indicator
            
        except Exception as e:
            logger.error(f"Error checking directory safety: {e}")
            return False
    
    def _get_safe_environment(self) -> Dict[str, str]:
        """Get a safe environment for command execution"""
        env = os.environ.copy()
        
        # Remove sensitive environment variables
        sensitive_vars = [
            'PATH', 'PYTHONPATH', 'NODE_PATH', 'JAVA_HOME', 'ANDROID_HOME',
            'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'GITHUB_TOKEN',
            'DOCKER_HOST', 'KUBECONFIG'
        ]
        
        for var in sensitive_vars:
            if var in env:
                env[var] = "***MASKED***"
        
        return env
    
    def _check_rate_limit(self) -> bool:
        """Check rate limiting for commands"""
        import time
        
        current_time = time.time()
        minute_ago = current_time - 60
        
        # Clean old entries
        self.rate_limit = {k: v for k, v in self.rate_limit.items() if v > minute_ago}
        
        # Check current rate
        if len(self.rate_limit) >= self.max_commands_per_minute:
            return False
        
        # Add current command
        self.rate_limit[current_time] = current_time
        
        return True
    
    def get_help_text(self) -> str:
        """Get help text showing allowed commands"""
        help_text = "🔒 Secure Command Executor Help\n\n"
        help_text += "📋 Allowed Command Categories:\n\n"
        
        for category, commands in self.ALLOWED_COMMANDS.items():
            help_text += f"🔹 {category.replace('_', ' ').title()}:\n"
            for cmd in commands:
                help_text += f"   • {cmd}\n"
            help_text += "\n"
        
        help_text += "💡 Usage:\n"
        help_text += "• Commands starting with '!' execute as terminal commands\n"
        help_text += "• All commands are validated against security whitelist\n"
        help_text += "• Output is automatically sanitized for security\n"
        help_text += "• Rate limiting: max 30 commands per minute\n\n"
        
        help_text += "🛡️ Security Features:\n"
        help_text += "• Command whitelisting\n"
        help_text += "• Input validation\n"
        help_text += "• Output sanitization\n"
        help_text += "• Path restrictions\n"
        help_text += "• Rate limiting\n"
        help_text += "• Audit logging"
        
        return help_text

# Global instance
_secure_executor = None

def get_secure_executor() -> SecureExecutor:
    """Get global secure executor instance"""
    global _secure_executor
    if _secure_executor is None:
        _secure_executor = SecureExecutor()
    return _secure_executor 