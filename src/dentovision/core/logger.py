import logging
import sys
from logging.handlers import RotatingFileHandler
import os
from core.config import settings

def setup_logger() -> logging.Logger:
    """
    Configures and returns a centralized logger.
    Supports console logging and rotating file logging.
    """
    logger = logging.getLogger("dentovision")
    
    # Avoid duplicate handlers if setup_logger is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()
        
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
    
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File Handler with Rotation (10 MB per file, keep 5 backups)
    log_file_path = os.path.join(settings.log_dir, "app.log")
    file_handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Prevent propagation to the root logger
    logger.propagate = False
    
    return logger

logger = setup_logger()
