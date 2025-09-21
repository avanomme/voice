#!/usr/bin/env python3
"""
Error Logging System for Voice Assistant
Centralized error logging with file output and console display
"""

import logging
import sys
import os
from pathlib import Path
from datetime import datetime
import traceback
from typing import Optional

class VoiceAssistantLogger:
    def __init__(self, log_dir: Optional[Path] = None):
        """
        Initialize the logging system

        Args:
            log_dir: Directory to store log files. Defaults to ~/.local/share/voice_assistant/logs/
        """
        if log_dir is None:
            self.log_dir = Path.home() / ".local" / "share" / "voice_assistant" / "logs"
        else:
            self.log_dir = log_dir

        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging configuration
        self.setup_logging()

    def setup_logging(self):
        """Configure logging with file and console handlers"""

        # Create log file paths
        error_log_file = self.log_dir / "errors.log"
        general_log_file = self.log_dir / "voice_assistant.log"

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # Remove existing handlers to avoid duplicates
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # File handler for errors only
        error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        error_handler.setFormatter(error_formatter)

        # File handler for all logs
        general_handler = logging.FileHandler(general_log_file, encoding='utf-8')
        general_handler.setLevel(logging.INFO)
        general_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        general_handler.setFormatter(general_formatter)

        # Console handler for important messages
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.WARNING)
        console_formatter = logging.Formatter(
            '%(levelname)s - %(name)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)

        # Add handlers to root logger
        root_logger.addHandler(error_handler)
        root_logger.addHandler(general_handler)
        root_logger.addHandler(console_handler)

        # Log startup
        logging.info("Voice Assistant logging system initialized")
        logging.info(f"Error logs: {error_log_file}")
        logging.info(f"General logs: {general_log_file}")

    def log_exception(self, exception: Exception, context: str = ""):
        """
        Log an exception with full traceback

        Args:
            exception: The exception to log
            context: Additional context about where the exception occurred
        """
        logger = logging.getLogger(__name__)

        error_msg = f"Exception in {context}: {str(exception)}" if context else f"Exception: {str(exception)}"

        # Log the exception with traceback
        logger.error(error_msg, exc_info=True)

        # Also log to a separate exception file
        exception_file = self.log_dir / "exceptions.log"
        with open(exception_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Context: {context}\n")
            f.write(f"Exception: {str(exception)}\n")
            f.write(f"Traceback:\n")
            traceback.print_exc(file=f)
            f.write(f"{'='*80}\n")

    def log_tts_error(self, engine: str, voice: str, error: Exception):
        """Log TTS-specific errors"""
        logger = logging.getLogger(f"tts.{engine}")
        logger.error(f"TTS Error - Engine: {engine}, Voice: {voice}, Error: {str(error)}")

    def log_wake_word_error(self, error: Exception):
        """Log wake word detection errors"""
        logger = logging.getLogger("wake_word")
        logger.error(f"Wake word detection error: {str(error)}")

    def log_audio_error(self, operation: str, error: Exception):
        """Log audio processing errors"""
        logger = logging.getLogger("audio")
        logger.error(f"Audio {operation} error: {str(error)}")

    def log_web_interface_error(self, endpoint: str, error: Exception):
        """Log web interface errors"""
        logger = logging.getLogger("web_interface")
        logger.error(f"Web interface error at {endpoint}: {str(error)}")

    def get_recent_errors(self, limit: int = 50) -> list:
        """
        Get recent error log entries

        Args:
            limit: Maximum number of recent entries to return

        Returns:
            List of recent error log entries
        """
        error_log_file = self.log_dir / "errors.log"

        if not error_log_file.exists():
            return []

        try:
            with open(error_log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return lines[-limit:] if len(lines) > limit else lines
        except Exception as e:
            logging.error(f"Failed to read error log: {e}")
            return []

# Global logger instance
_global_logger: Optional[VoiceAssistantLogger] = None

def get_logger() -> VoiceAssistantLogger:
    """Get or create the global logger instance"""
    global _global_logger
    if _global_logger is None:
        _global_logger = VoiceAssistantLogger()
    return _global_logger

def log_exception(exception: Exception, context: str = ""):
    """Convenience function to log an exception"""
    get_logger().log_exception(exception, context)

def log_tts_error(engine: str, voice: str, error: Exception):
    """Convenience function to log TTS errors"""
    get_logger().log_tts_error(engine, voice, error)

def log_wake_word_error(error: Exception):
    """Convenience function to log wake word errors"""
    get_logger().log_wake_word_error(error)

def log_audio_error(operation: str, error: Exception):
    """Convenience function to log audio errors"""
    get_logger().log_audio_error(operation, error)

def log_web_interface_error(endpoint: str, error: Exception):
    """Convenience function to log web interface errors"""
    get_logger().log_web_interface_error(endpoint, error)