import logging
import logging.handlers
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[95m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record):
        levelname = record.levelname
        message = super().format(record)
        color = self.COLORS.get(levelname, self.COLORS["RESET"])
        return color + message + self.COLORS["RESET"]


def get_project_name():
    """
    Extract project name from the log file path or use the directory name as fallback.
    Returns:
        str: Project name
    """
    # Try to get from environment variable first
    log_file = os.getenv("LOG_FILE_PATH", "")
    if log_file:
        # Extract project name from log file path
        base_name = os.path.basename(log_file)
        project_name = base_name.split(".")[0]  # Remove extension
        if project_name:
            return project_name

    # Fallback: use the name of the project directory
    project_dir = os.path.basename(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    return project_dir


def setup_logging(level=logging.INFO, log_file=None, propagate=False, include_location=True):
    """Set up logging with colored console output and file output.
    
    Args:
        level: The logging level, default is INFO
        log_file: The log file path, default is None (auto-generated)
        propagate: Whether to propagate logs to parent handlers, default is False
        include_location: Whether to include filename and line number, default is True
    """
    # Create formatters with file and line number information
    if include_location:
        log_format = '[%(asctime)s] %(levelname)-8s %(filename)s:%(lineno)d: %(message)s'
    else:
        log_format = '[%(asctime)s] %(levelname)-8s: %(message)s'
    
    formatter = logging.Formatter(log_format, '%Y-%m-%d %H:%M:%S')
    
    # Create a colored formatter for console output
    try:
        import colorlog
        if include_location:
            colored_format = '%(log_color)s[%(asctime)s] %(levelname)-8s %(filename)s:%(lineno)d: %(message)s%(reset)s'
        else:
            colored_format = '%(log_color)s[%(asctime)s] %(levelname)-8s: %(message)s%(reset)s'
        
        colored_formatter = colorlog.ColoredFormatter(
            colored_format,
            '%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
    except ImportError:
        # If colorlog is not available, use our custom ColoredFormatter
        colored_formatter = ColoredFormatter(log_format, '%Y-%m-%d %H:%M:%S')
    
    if log_file is None:
        # Get log file path, if on a Mac, use the parent path of the current path
        if sys.platform == 'darwin':
            log_dir = os.path.join(os.path.expanduser('~'), 'Library', 'Logs', 'anp-examples')
        else:
            log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'logs')
        
        # Create logs directory if it doesn't exist and set permissions
        try:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
                
                # Set directory permissions to 755
                if sys.platform != 'win32':
                    os.chmod(log_dir, 0o755)
        except Exception as e:
            # If creation fails, use a fallback log directory
            print(f"Error creating log directory {log_dir}: {e}")
            log_dir = os.path.join(os.path.expanduser('~'), 'logs')
            os.makedirs(log_dir, exist_ok=True)
        
        # Generate log filename (with date)
        log_file = os.path.join(log_dir, 'anp-examples.log')
    
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Configure colored console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(colored_formatter)
    logger.addHandler(console_handler)
    
    # Configure file handler with the same format (but without color)
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logger.info(f"Logging to file: {log_file}")
    except Exception as e:
        logger.error(f"Failed to set up file logging to {log_file}: {e}")
    
    # Prevent log messages from propagating to root logger
    if not propagate:
        logger.propagate = False
    
    return logger


def configure_all_loggers(level=logging.INFO, include_location=True):
    """Configure all existing and future loggers to use the same format with file and line information.
    
    Args:
        level: The logging level to apply to all loggers
        include_location: Whether to include filename and line number
    """
    # Set up the root logger first
    setup_logging(level=level, include_location=include_location)
    
    # Get all existing loggers and configure them
    existing_loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    
    for logger in existing_loggers:
        logger.setLevel(level)
        # Remove existing handlers to avoid duplication
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        # Let the root logger handle all messages
        logger.propagate = True
    
    # Configure specific third-party loggers if needed
    third_party_loggers = [
        'httpx',
        'httpcore', 
        'openai',
        'aiohttp',
        'urllib3',
        'requests'
    ]
    
    for logger_name in third_party_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.propagate = True


def set_log_color_level(level=logging.INFO, include_location=True, configure_all=True):
    """Set up logging with optional file/line information and global configuration.
    
    Args:
        level: The logging level
        include_location: Whether to include filename and line number
        configure_all: Whether to configure all existing loggers
    """
    if configure_all:
        configure_all_loggers(level=level, include_location=include_location)
    else:
        setup_logging(level=level, include_location=include_location)
    
    return logging.getLogger()


# For backward compatibility, keep the original function but with enhanced features
def setup_enhanced_logging(level=logging.DEBUG):
    """Enhanced logging setup with file and line number information for all loggers."""
    return set_log_color_level(level=level, include_location=True, configure_all=True)
