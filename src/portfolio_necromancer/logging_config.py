"""
Portfolio Necromancer - Logging configuration
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

import logging
import sys
from typing import Optional


def setup_logging(level: Optional[str] = None, log_file: Optional[str] = None):
    """Configure structured logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
    """
    # Determine log level
    log_level = getattr(logging, (level or 'INFO').upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('googleapiclient').setLevel(logging.WARNING)
    logging.getLogger('google.auth').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.
    
    Args:
        name: Name of the module (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
