"""
A utility module for logging in Python.
"""
import logging

class Logger:
    """A utility class for setting up and managing loggers."""
    
    _loggers = {}  # Cache for loggers to avoid duplicate handlers

    @staticmethod
    def get_logger(name: str, level: str = "INFO") -> logging.Logger:
        """Get or create a logger with the specified name and level."""
        if name not in Logger._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(level)
            if not logger.handlers:  # Avoid adding multiple handlers
                handler = logging.StreamHandler()
                handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
                logger.addHandler(handler)
            Logger._loggers[name] = logger
        return Logger._loggers[name]