from sys import stderr
from loguru import logger
from pathlib import Path

from config.environment import application_settings, logger_settings

LOG_FILE_PATH = Path(logger_settings.LOG_DIR, f"{application_settings.APP_NAME}-v{application_settings.APP_VERSION}.log")


def init_logger(log_file_path=LOG_FILE_PATH,
                std_level=logger_settings.STD_LEVEL,
                file_level=logger_settings.FILE_LEVEL,
                rotation=logger_settings.LOG_ROTATION,
                compression=logger_settings.LOG_COMPRESSION):
    logger.remove()
    logger.add(
        stderr,
        format=logger_settings.LOG_FORMAT,
        level=std_level,
    )
    logger.add(
        log_file_path,
        format=logger_settings.LOG_FORMAT,
        level=file_level,
        rotation=rotation,
        compression=compression
    )
    return logger
