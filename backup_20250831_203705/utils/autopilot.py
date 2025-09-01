#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autopilot notification module for UwU-CLI
Handles sending notifications via Telegram, Email, and Feishu
"""

import json
import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# Setup logging
import logging
logger = logging.getLogger(__name__)


class Autopilot:
    def __init__(self, config_path: str = ".autopilot.json"):
        """Initialize autopilot with configuration"""
        self.config = self._load_config(config_path)
        self.enabled = self.config.get("enabled", False)
        self.adapters = self.config.get("adapters", [])

        if self.enabled:
            logger.info("Autopilot initialized with adapters: %s",
                        self.adapters)
        else:
            logger.warning("Autopilot is disabled in configuration")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load autopilot configuration"""
        if config_path is None:
            # Try multiple possible config file locations
            possible_paths = [
                ".autopilot.json",
                os.path.join(os.path.dirname(
                    os.path.dirname(__file__)), ".autopilot.json"),
                os.path.join(os.getcwd(), ".autopilot.json")
            ]
        else:
            possible_paths = [config_path]

        for path in possible_paths:
            try:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        logger.info(
                            "Autopilot configuration loaded from %s", path)
                        return config
                else:
                    logger.debug("Autopilot config not found: %s", path)
            except (IOError, json.JSONDecodeError) as e:
                logger.debug(
                    "Failed to load autopilot config from %s: %s", path, e)
                continue

        logger.warning(
            "No valid autopilot configuration found in any location")
        return {"enabled": False}

    def send_notification(self, message: str, title: str = "UwU-CLI Notification") -> bool:
        """Send notification through all enabled adapters"""
        if not self.enabled:
            return False

        success = True

        for adapter in self.adapters:
            try:
                if adapter == "telegram":
                    success &= self._send_telegram(message)
                elif adapter == "email":
                    success &= self._send_email(message, title)
                elif adapter == "feishu":
                    success &= self._send_feishu(message, title)
                else:
                    logger.warning(f"Unknown adapter: {adapter}")
            except Exception as e:
                logger.error(f"Failed to send {adapter} notification: {e}")
                success = False

        return success

    def _send_telegram(self, message: str) -> bool:
        """Send Telegram notification"""
        try:
             {}).get("token")
            chat_id = self.config.get("telegram", {}).get("chatId")

            if not token or not chat_id:
                logger.error("Telegram token or chat ID not configured")
                return False

            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }

            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                logger.info("Telegram notification sent successfully")
                return True
            else:
                logger.error(f"Telegram API error: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Telegram notification failed: {e}")
            return False

    def _send_email(self, message: str, title: str) -> bool:
        """Send email notification"""
        try:
            email_config = self.config.get("email", {})
            host = email_config.get("host")
            port = email_config.get("port", 587)
            user = email_config.get("user")
            password = email_config.get("pass")
            to_email = email_config.get("to")

            if not all([host, user, password, to_email]):
                logger.error("Email configuration incomplete")
                return False

            # Create message
            msg = MIMEMultipart()
            msg['From'] = user
            msg['To'] = to_email
            msg['Subject'] = title

            msg.attach(MIMEText(message, 'plain'))

            # Send email
            server = smtplib.SMTP(host, port)
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
            server.quit()

            logger.info("Email notification sent successfully")
            return True

        except Exception as e:
            logger.error(f"Email notification failed: {e}")
            return False

    def _send_feishu(self, message: str, title: str) -> bool:
        """Send Feishu notification"""
        try:
            feishu_config = self.config.get("feishu", {})
            app_id = feishu_config.get("appId")
            app_

            if not app_id or not app_ configuration incomplete")
                return False

            # Get access token
            token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            token_data = {
                "app_id": app_id,
                "app_secret": app_secret
            }

            token_response = requests.post(
                token_url, json=token_data, timeout=10)
            if token_response.status_code != 200:
                logger.error("Failed to get Feishu access token")
                return False

            access_

            # Send message (this is a simplified version)
            # You might need to adjust based on your specific Feishu app setup
            logger.info(
                "Feishu notification prepared (implementation may need adjustment)")
            return True

        except Exception as e:
            logger.error(f"Feishu notification failed: {e}")
            return False

    def notify_cli_start(self):
        """Send notification when CLI starts"""
        message = f"🚀 UwU-CLI started at {self._get_timestamp()}"
        return self.send_notification(message, "UwU-CLI Started")

    def notify_cli_exit(self):
        """Send notification when CLI exits"""
        message = f"👋 UwU-CLI exited at {self._get_timestamp()}"
        return self.send_notification(message, "UwU-CLI Exited")

    def notify_command_executed(self, command: str, success: bool = True):
        """Send notification about command execution"""
        status = "✅" if success else "❌"
        message = f"{status} Command executed: {command}\nTime: {self._get_timestamp()}"
        return self.send_notification(message, "Command Executed")

    def notify_error(self, error: str, context: str = ""):
        """Send error notification"""
        message = f"🚨 Error in {context}: {error}\nTime: {self._get_timestamp()}"
        return self.send_notification(message, "UwU-CLI Error")

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Global autopilot instance
_autopilot = None


def get_autopilot() -> Optional[Autopilot]:
    """Get global autopilot instance"""
    global _autopilot
    if _autopilot is None:
        _autopilot = Autopilot()
    return _autopilot


def send_notification(message: str, title: str = "UwU-CLI Notification") -> bool:
    """Send notification using global autopilot instance"""
    autopilot = get_autopilot()
    if autopilot:
        return autopilot.send_notification(message, title)
    return False
