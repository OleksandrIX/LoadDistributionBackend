from loguru import logger
from config import (logger as logger_config)


@logger.catch
def main():
    logger_config.init_logger()
    logger.info("Service started.")


if __name__ == "__main__":
    main()
