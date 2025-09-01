#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Error Handler for UwU-CLI
Implements comprehensive error handling, logging, and user-friendly error messages
"""

import os
import sys
import logging
import traceback
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path

logger = logging.getLogger(__name__)


class ErrorCategory:
    """Error categories for classification"""
    COMMAND_EXECUTION = "command_execution"
    FILE_OPERATION = "file_operation"
    NETWORK = "network"
    PERMISSION = "permission"
    VALIDATION = "validation"
    SYSTEM = "system"
    UNKNOWN = "unknown"


class ErrorSeverity:
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorHandler:
    """Comprehensive error handling system"""
    
    def __init__(self, log_dir: str = "tmp/logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Error log files
        self.error_log_file = self.log_dir / "errors.log"
        self.debug_log_file = self.log_dir / "debug.log"
        self.audit_log_file = self.log_dir / "audit.log"
        
        # Error statistics
        self.error_counts = {}
        self.error_history = []
        self.max_error_history = 1000
        
        # Setup logging
        self._setup_logging()
        
        # Error handlers
        self.error_handlers = {}
        self._register_default_handlers()
        
        # Recovery strategies
        self.recovery_strategies = {}
        self._register_recovery_strategies()
        
        logger.info("Enhanced error handler initialized")
    
    def _setup_logging(self):
        """Setup comprehensive logging system"""
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Error log handler
        error_handler = logging.FileHandler(self.error_log_file)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        
        # Debug log handler
        debug_handler = logging.FileHandler(self.debug_log_file)
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(detailed_formatter)
        
        # Audit log handler
        audit_handler = logging.FileHandler(self.audit_log_file)
        audit_handler.setLevel(logging.INFO)
        audit_handler.setFormatter(simple_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(simple_formatter)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(error_handler)
        root_logger.addHandler(debug_handler)
        root_logger.addHandler(audit_handler)
        root_logger.addHandler(console_handler)
    
    def _register_default_handlers(self):
        """Register default error handlers"""
        self.register_error_handler(
            ErrorCategory.COMMAND_EXECUTION,
            self._handle_command_execution_error
        )
        self.register_error_handler(
            ErrorCategory.FILE_OPERATION,
            self._handle_file_operation_error
        )
        self.register_error_handler(
            ErrorCategory.NETWORK,
            self._handle_network_error
        )
        self.register_error_handler(
            ErrorCategory.PERMISSION,
            self._handle_permission_error
        )
        self.register_error_handler(
            ErrorCategory.VALIDATION,
            self._handle_validation_error
        )
        self.register_error_handler(
            ErrorCategory.SYSTEM,
            self._handle_system_error
        )
    
    def _register_recovery_strategies(self):
        """Register recovery strategies for different error types"""
        self.recovery_strategies = {
            ErrorCategory.COMMAND_EXECUTION: [
                "Retry command with different parameters",
                "Check command syntax and try again",
                "Verify required dependencies are installed"
            ],
            ErrorCategory.FILE_OPERATION: [
                "Check file permissions",
                "Verify file path exists",
                "Ensure sufficient disk space"
            ],
            ErrorCategory.NETWORK: [
                "Check internet connection",
                "Verify API endpoints are accessible",
                "Retry operation after delay"
            ],
            ErrorCategory.PERMISSION: [
                "Run with elevated privileges",
                "Check user permissions",
                "Verify file/directory access rights"
            ],
            ErrorCategory.VALIDATION: [
                "Review input parameters",
                "Check data format requirements",
                "Verify configuration settings"
            ]
        }
    
    def register_error_handler(self, category: str, handler: Callable):
        """Register a custom error handler for a category"""
        self.error_handlers[category] = handler
        logger.debug(f"Registered error handler for category: {category}")
    
    def handle_error(self, error: Exception, category: str = ErrorCategory.UNKNOWN,
                    context: Dict[str, Any] = None, severity: str = ErrorSeverity.MEDIUM) -> str:
        """Handle an error comprehensively"""
        try:
            # Create error record
            error_record = self._create_error_record(error, category, context, severity)
            
            # Log error
            self._log_error(error_record)
            
            # Update statistics
            self._update_error_statistics(category, severity)
            
            # Execute error handler
            error_message = self._execute_error_handler(error_record)
            
            # Attempt recovery
            recovery_suggestions = self._get_recovery_suggestions(category)
            
            # Return user-friendly error message
            return self._format_error_message(error_message, recovery_suggestions, severity)
            
        except Exception as e:
            # Fallback error handling
            logger.critical(f"Error in error handler: {e}")
            return f"An unexpected error occurred: {str(error)}"
    
    def _create_error_record(self, error: Exception, category: str,
                           context: Dict[str, Any], severity: str) -> Dict[str, Any]:
        """Create a comprehensive error record"""
        return {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'category': category,
            'severity': severity,
            'context': context or {},
            'traceback': traceback.format_exc(),
            'system_info': self._get_system_info()
        }
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information for error context"""
        return {
            'platform': sys.platform,
            'python_version': sys.version,
            'working_directory': os.getcwd(),
            'user': os.getenv('USERNAME') or os.getenv('USER'),
            'environment': os.getenv('ENVIRONMENT', 'development')
        }
    
    def _log_error(self, error_record: Dict[str, Any]):
        """Log error to appropriate log files"""
        # Log to error log
        logger.error(f"Error occurred: {error_record['error_type']}: {error_record['error_message']}")
        
        # Log to debug log with full details
        logger.debug(f"Full error details: {json.dumps(error_record, indent=2)}")
        
        # Log to audit log
        logger.info(f"Error logged: {error_record['category']} - {error_record['severity']}")
        
        # Store in memory for statistics
        self.error_history.append(error_record)
        if len(self.error_history) > self.max_error_history:
            self.error_history.pop(0)
    
    def _update_error_statistics(self, category: str, severity: str):
        """Update error statistics"""
        if category not in self.error_counts:
            self.error_counts[category] = {'total': 0, 'by_severity': {}}
        
        self.error_counts[category]['total'] += 1
        
        if severity not in self.error_counts[category]['by_severity']:
            self.error_counts[category]['by_severity'][severity] = 0
        self.error_counts[category]['by_severity'][severity] += 1
    
    def _execute_error_handler(self, error_record: Dict[str, Any]) -> str:
        """Execute the appropriate error handler"""
        category = error_record['category']
        handler = self.error_handlers.get(category)
        
        if handler:
            try:
                return handler(error_record)
            except Exception as e:
                logger.error(f"Error handler failed: {e}")
                return f"Error occurred: {error_record['error_message']}"
        else:
            return f"Error occurred: {error_record['error_message']}"
    
    def _get_recovery_suggestions(self, category: str) -> List[str]:
        """Get recovery suggestions for error category"""
        return self.recovery_strategies.get(category, [
            "Check the error details above",
            "Review system logs for more information",
            "Contact support if the problem persists"
        ])
    
    def _format_error_message(self, error_message: str, 
                            recovery_suggestions: List[str], severity: str) -> str:
        """Format error message for user display"""
        severity_icons = {
            ErrorSeverity.LOW: "ℹ️",
            ErrorSeverity.MEDIUM: "⚠️",
            ErrorSeverity.HIGH: "🚨",
            ErrorSeverity.CRITICAL: "💥"
        }
        
        icon = severity_icons.get(severity, "❌")
        
        message = f"{icon} **Error ({severity.upper()}):** {error_message}\n\n"
        
        if recovery_suggestions:
            message += "🔧 **Recovery Suggestions:**\n"
            for suggestion in recovery_suggestions:
                message += f"   • {suggestion}\n"
        
        return message
    
    # Default error handlers
    def _handle_command_execution_error(self, error_record: Dict[str, Any]) -> str:
        """Handle command execution errors"""
        error_msg = error_record['error_message']
        
        if "command not found" in error_msg.lower():
            return "Command not found. Please check the command name and try again."
        elif "permission denied" in error_msg.lower():
            return "Permission denied. You may need elevated privileges to run this command."
        elif "no such file" in error_msg.lower():
            return "File or directory not found. Please verify the path exists."
        else:
            return f"Command execution failed: {error_msg}"
    
    def _handle_file_operation_error(self, error_record: Dict[str, Any]) -> str:
        """Handle file operation errors"""
        error_msg = error_record['error_message']
        
        if "permission denied" in error_msg.lower():
            return "File access denied. Check file permissions and try again."
        elif "no space left" in error_msg.lower():
            return "Insufficient disk space. Free up some space and try again."
        elif "file not found" in error_msg.lower():
            return "File not found. Please verify the file path is correct."
        else:
            return f"File operation failed: {error_msg}"
    
    def _handle_network_error(self, error_record: Dict[str, Any]) -> str:
        """Handle network-related errors"""
        error_msg = error_record['error_message']
        
        if "connection refused" in error_msg.lower():
            return "Connection refused. Check if the service is running and accessible."
        elif "timeout" in error_msg.lower():
            return "Connection timeout. Check your internet connection and try again."
        elif "dns" in error_msg.lower():
            return "DNS resolution failed. Check your internet connection and DNS settings."
        else:
            return f"Network operation failed: {error_msg}"
    
    def _handle_permission_error(self, error_record: Dict[str, Any]) -> str:
        """Handle permission-related errors"""
        error_msg = error_record['error_message']
        
        if "access denied" in error_msg.lower():
            return "Access denied. You may need administrator privileges."
        elif "read-only" in error_msg.lower():
            return "File system is read-only. Check file system permissions."
        else:
            return f"Permission error: {error_msg}"
    
    def _handle_validation_error(self, error_record: Dict[str, Any]) -> str:
        """Handle validation errors"""
        error_msg = error_record['error_message']
        
        if "invalid" in error_msg.lower():
            return "Invalid input provided. Please check your parameters and try again."
        elif "required" in error_msg.lower():
            return "Required parameter missing. Please provide all required parameters."
        else:
            return f"Validation error: {error_msg}"
    
    def _handle_system_error(self, error_record: Dict[str, Any]) -> str:
        """Handle system-level errors"""
        error_msg = error_record['error_message']
        
        if "memory" in error_msg.lower():
            return "Insufficient memory. Close other applications and try again."
        elif "disk" in error_msg.lower():
            return "Disk error detected. Check disk health and try again."
        else:
            return f"System error: {error_msg}"
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get comprehensive error statistics"""
        total_errors = sum(cat['total'] for cat in self.error_counts.values())
        
        # Calculate severity distribution
        severity_distribution = {}
        for category_data in self.error_counts.values():
            for severity, count in category_data['by_severity'].items():
                severity_distribution[severity] = severity_distribution.get(severity, 0) + count
        
        # Get recent errors
        recent_errors = self.error_history[-10:] if self.error_history else []
        
        return {
            'total_errors': total_errors,
            'error_categories': self.error_counts,
            'severity_distribution': severity_distribution,
            'recent_errors': recent_errors,
            'log_files': {
                'error_log': str(self.error_log_file),
                'debug_log': str(self.debug_log_file),
                'audit_log': str(self.audit_log_file)
            }
        }
    
    def clear_error_history(self):
        """Clear error history"""
        self.error_history.clear()
        self.error_counts.clear()
        logger.info("Error history cleared")
    
    def export_error_logs(self, filepath: str) -> bool:
        """Export error logs to file"""
        try:
            export_data = {
                'export_time': datetime.now().isoformat(),
                'statistics': self.get_error_statistics(),
                'error_history': self.error_history
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Error logs exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to export error logs: {e}")
            return False
    
    def enable_debug_mode(self, enabled: bool = True):
        """Enable or disable debug mode"""
        if enabled:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.info("Debug mode enabled")
        else:
            logging.getLogger().setLevel(logging.INFO)
            logger.info("Debug mode disabled")


# Global error handler instance
_error_handler = None


def get_error_handler() -> ErrorHandler:
    """Get global error handler instance"""
    global _error_handler
    if _error_handler is None:
        _error_handler = ErrorHandler()
    return _error_handler


def handle_error(error: Exception, category: str = ErrorCategory.UNKNOWN,
                context: Dict[str, Any] = None, severity: str = ErrorSeverity.MEDIUM) -> str:
    """Global error handling function"""
    handler = get_error_handler()
    return handler.handle_error(error, category, context, severity) 