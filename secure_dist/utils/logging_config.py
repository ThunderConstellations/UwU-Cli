#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Centralized Logging Configuration for UwU-CLI
Provides consistent logging setup across all modules
"""

import os
import sys
import logging
import logging.handlers
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

# Global logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'json': {
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "function": "%(funcName)s", "line": %(lineno)d, "message": "%(message)s"}',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': 'tmp/logs/errors.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        },
        'debug_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'tmp/logs/debug.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        },
        'audit_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'filename': 'tmp/logs/audit.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        },
        'performance_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'json',
            'filename': 'tmp/logs/performance.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,
            'encoding': 'utf8'
        }
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console', 'error_file', 'debug_file', 'audit_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'utils': {
            'handlers': ['console', 'error_file', 'debug_file', 'audit_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'utils.telegram_controller': {
            'handlers': ['console', 'error_file', 'debug_file', 'audit_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'utils.autopilot': {
            'handlers': ['console', 'error_file', 'debug_file', 'audit_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'utils.error_handler': {
            'handlers': ['console', 'error_file', 'debug_file', 'audit_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'utils.system_improvements': {
            'handlers': ['console', 'error_file', 'debug_file', 'audit_file', 'performance_file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

def setup_logging(config: Optional[Dict[str, Any]] = None, log_level: str = 'INFO') -> None:
    """
    Setup centralized logging configuration
    
    Args:
        config: Custom logging configuration (optional)
        log_level: Global log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Ensure log directory exists
    log_dir = Path('tmp/logs')
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Update log level in config
    if config is None:
        config = LOGGING_CONFIG.copy()
    
    # Set global log level
    config['loggers']['']['level'] = log_level.upper()
    
    # Apply configuration
    try:
        logging.config.dictConfig(config)
        logging.getLogger().info(f"Logging system initialized with level: {log_level.upper()}")
    except Exception as e:
        # Fallback to basic logging if dictConfig fails
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('tmp/logs/fallback.log', encoding='utf-8')
            ]
        )
        logging.getLogger().warning(f"Failed to apply advanced logging config: {e}. Using fallback.")

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

def set_log_level(logger_name: str, level: str) -> None:
    """
    Set log level for a specific logger
    
    Args:
        logger_name: Name of the logger to configure
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    try:
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, level.upper()))
        logger.info(f"Log level set to {level.upper()}")
    except Exception as e:
        logging.getLogger().error(f"Failed to set log level for {logger_name}: {e}")

def enable_debug_mode() -> None:
    """Enable debug mode for all loggers"""
    set_log_level('', 'DEBUG')
    logging.getLogger().info("Debug mode enabled for all loggers")

def disable_debug_mode() -> None:
    """Disable debug mode for all loggers"""
    set_log_level('', 'INFO')
    logging.getLogger().info("Debug mode disabled for all loggers")

def log_performance_metric(metric_name: str, value: Any, unit: str = '', context: Dict[str, Any] = None) -> None:
    """
    Log performance metrics to the performance log
    
    Args:
        metric_name: Name of the metric
        value: Metric value
        unit: Unit of measurement (optional)
        context: Additional context information (optional)
    """
    logger = logging.getLogger('utils.system_improvements')
    
    log_data = {
        'metric': metric_name,
        'value': value,
        'unit': unit,
        'timestamp': datetime.now().isoformat(),
        'context': context or {}
    }
    
    logger.info(f"PERFORMANCE: {log_data}")

def log_security_event(event_type: str, description: str, severity: str = 'INFO', context: Dict[str, Any] = None) -> None:
    """
    Log security events to the audit log
    
    Args:
        event_type: Type of security event
        description: Description of the event
        severity: Event severity (INFO, WARNING, ERROR, CRITICAL)
        context: Additional context information (optional)
    """
    logger = logging.getLogger('utils.error_handler')
    
    log_data = {
        'event_type': event_type,
        'description': description,
        'severity': severity,
        'timestamp': datetime.now().isoformat(),
        'context': context or {}
    }
    
    if severity.upper() == 'ERROR':
        logger.error(f"SECURITY: {log_data}")
    elif severity.upper() == 'WARNING':
        logger.warning(f"SECURITY: {log_data}")
    else:
        logger.info(f"SECURITY: {log_data}")

def log_telegram_event(event_type: str, description: str, success: bool = True, context: Dict[str, Any] = None) -> None:
    """
    Log Telegram-related events
    
    Args:
        event_type: Type of Telegram event
        description: Description of the event
        success: Whether the event was successful
        context: Additional context information (optional)
    """
    logger = logging.getLogger('utils.telegram_controller')
    
    log_data = {
        'event_type': event_type,
        'description': description,
        'success': success,
        'timestamp': datetime.now().isoformat(),
        'context': context or {}
    }
    
    if success:
        logger.info(f"TELEGRAM: {log_data}")
    else:
        logger.error(f"TELEGRAM: {log_data}")

def log_cursor_event(event_type: str, description: str, success: bool = True, context: Dict[str, Any] = None) -> None:
    """
    Log Cursor editor events
    
    Args:
        event_type: Type of Cursor event
        description: Description of the event
        success: Whether the event was successful
        context: Additional context information (optional)
    """
    logger = logging.getLogger('utils.cursor_controller')
    
    log_data = {
        'event_type': event_type,
        'description': description,
        'success': success,
        'timestamp': datetime.now().isoformat(),
        'context': context or {}
    }
    
    if success:
        logger.info(f"CURSOR: {log_data}")
    else:
        logger.error(f"CURSOR: {log_data}")

def cleanup_old_logs(max_age_days: int = 30) -> None:
    """
    Clean up old log files
    
    Args:
        max_age_days: Maximum age of log files in days
    """
    try:
        log_dir = Path('tmp/logs')
        if not log_dir.exists():
            return
        
        cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 60 * 60)
        
        for log_file in log_dir.glob('*.log.*'):
            if log_file.stat().st_mtime < cutoff_time:
                log_file.unlink()
                logging.getLogger().info(f"Cleaned up old log file: {log_file}")
                
    except Exception as e:
        logging.getLogger().error(f"Failed to cleanup old logs: {e}")

# Initialize logging when module is imported
if __name__ != '__main__':
    setup_logging() 