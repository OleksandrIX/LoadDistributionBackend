import os
from sys import stderr
from loguru import logger
from pathlib import Path

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSSZZ}</green> "
    "| <level>{level:>8}</level> "
    "| <cyan>[{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}]</cyan> "
    "--- <level>{message}</level>"
)

APP_NAME = os.environ.get("APP_NAME") or "excel-parser"
LOG_DIR = os.environ.get("LOG_DIR") or "logs"
LOG_FILE_PATH = Path(LOG_DIR, f"{APP_NAME}.log")

STD_LEVEL = os.environ.get("STD_LEVEL") or "TRACE"
FILE_LEVEL = os.environ.get("FILE_LEVEL") or "INFO"
LOG_ROTATION = os.environ.get("LOG_ROTATION") or "12:00"
LOG_COMPRESSION = os.environ.get("LOG_COMPRESSION") or "gz"


def init_logger(log_file_path=LOG_FILE_PATH,
                std_level=STD_LEVEL,
                file_level=FILE_LEVEL,
                rotation=LOG_ROTATION,
                compression=LOG_COMPRESSION):
    logger.remove()
    logger.add(
        stderr,
        format=LOG_FORMAT,
        level=std_level,
    )
    logger.add(
        log_file_path,
        format=LOG_FORMAT,
        level=file_level,
        rotation=rotation,
        compression=compression
    )
    return logger
