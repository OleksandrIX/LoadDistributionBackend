import logging

from sys import stderr
from pathlib import Path
from loguru import logger

from .environment import application_settings, logger_settings

LOG_FILE_PATH = Path(logger_settings.LOG_DIR,
                     f"{application_settings.APP_NAME}-v{application_settings.APP_VERSION}.log")


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        5: "TRACE",
        0: "NOTSET",
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class CustomizeLogger:
    @classmethod
    def make_logger(cls):
        logger = cls.customize_logging(
            LOG_FILE_PATH,
            level=logger_settings.LOG_LEVEL,
            rotation=logger_settings.LOG_ROTATION,
            compresion=logger_settings.LOG_COMPRESSION,
            format=logger_settings.LOG_FORMAT
        )
        return logger

    @classmethod
    def customize_logging(cls, filepath: Path, level: str, rotation: str, compresion: str, format: str):
        logger.remove()
        logger.add(
            stderr,
            level=level,
            format=format
        )

        logger.add(
            str(filepath),
            level=level,
            format=format,
            rotation=rotation,
            compression=compresion
        )

        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ["uvicorn", "uvicorn.error", "fastapi"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)
