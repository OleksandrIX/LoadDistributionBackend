import re
import sys
import time
from loguru import logger
from config import (logger as logger_config)
from utils import (read_excel, db_connect)

import uuid
import datetime
from models.department import Department


@logger.catch
def main():
    logger_config.init_logger()
    logger.info("Service started.")
    # read_excel.start()
    test()


def test():
    logger.debug("------- Start test -------")

    department = Department(
        id=uuid.uuid4(),
        department_code=22,
        department_name="22",
        specialization="22",
        created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    logger.debug(department.to_dict())

    logger.debug("------- End test   -------")


if __name__ == "__main__":
    main()
