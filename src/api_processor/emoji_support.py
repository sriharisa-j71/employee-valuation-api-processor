"""Emoji support detection and fallback handling"""
import os
import sys
from typing import Dict


def supports_emoji() -> bool:
    """
    Detect if the current terminal supports emoji display.
    
    Returns:
        bool: True if emoji is supported, False otherwise
    """
    # Check if we're in a CI environment (usually no emoji support)
    ci_indicators = ['CI', 'GITHUB_ACTIONS', 'GITLAB_CI', 'JENKINS_URL', 'TRAVIS']
    if any(os.getenv(indicator) for indicator in ci_indicators):
        return False
    
    # Check if stdout is redirected (pipes, files)
    if not sys.stdout.isatty():
        return False
    
    # Check terminal type
    term = os.getenv('TERM', '').lower()
    if term in ['dumb', 'unknown', '']:
        return False
    
    # Check for known terminals that don't support emoji well
    term_program = os.getenv('TERM_PROGRAM', '').lower()
    if term_program in ['mintty']:  # Git Bash on Windows
        return False
    
    # Check encoding
    encoding = sys.stdout.encoding
    if encoding and encoding.lower() not in ['utf-8', 'utf8']:
        return False
    
    # Default to emoji support for modern terminals
    return True


class EmojiHandler:
    """Handles emoji display with fallback support"""
    
    def __init__(self):
        self.emoji_enabled = supports_emoji()
        
        # Emoji mappings with fallbacks
        self.status_icons = {
            "pending": ("⏳", "[PENDING]"),
            "success": ("✅", "[SUCCESS]"),
            "failed": ("❌", "[FAILED]"),
            "warning": ("⚠️", "[WARNING]"),
            "info": ("ℹ️", "[INFO]"),
            "error": ("🚨", "[ERROR]"),
            "total": ("📊", "[TOTAL]"),
        }
        
        self.action_icons = {
            "loading": ("📁", "Loading"),
            "processing": ("⚙️", "Processing"),
            "report": ("📋", "Report"),
            "reset": ("🔄", "Reset"),
            "performance": ("📊", "Performance"),
            "validation": ("📊", "Validation"),
            "distribution": ("📈", "Distribution"),
            "failures": ("⚠️", "Failures"),
            "grade": ("🎯", "Grade"),
            "complete": ("✅", "Complete"),
        }
    
    def get_status_icon(self, status: str) -> str:
        """Get status icon with fallback"""
        emoji, fallback = self.status_icons.get(status.lower(), ("📋", f"[{status.upper()}]"))
        return emoji if self.emoji_enabled else fallback
    
    def get_action_icon(self, action: str) -> str:
        """Get action icon with fallback"""
        emoji, fallback = self.action_icons.get(action.lower(), ("", action.title()))
        return emoji if self.emoji_enabled else fallback
    
    def format_message(self, action: str, message: str) -> str:
        """Format message with appropriate icon"""
        icon = self.get_action_icon(action)
        if self.emoji_enabled and icon:
            return f"{icon} {message}"
        elif not self.emoji_enabled and icon:
            return f"{icon}: {message}"
        else:
            return message
    
    def format_status_row(self, status: str, title: str = None) -> str:
        """Format status row for tables"""
        icon = self.get_status_icon(status)
        if title:
            return f"{icon} {title}"
        else:
            return f"{icon} {status.title()}"


# Global instance
emoji_handler = EmojiHandler()