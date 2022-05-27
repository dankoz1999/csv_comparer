__version__ = "0.0.9"

import logging
import os
import sys

# log level
LOG_LEVEL = os.environ.get("LOG_LEVEL", "debug").upper()

def get_logger() -> logging.Logger:
    """
    utility function to get a unified logger for the whole project
    """
    logging.setLoggerClass(logging.Logger)
    logger = logging.getLogger("comparer")

    logger.setLevel(LOG_LEVEL)
    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] <%(name)s> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger