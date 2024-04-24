import os
import sys
from loguru import logger
from config import logger as logger_config


@logger.catch
def main():
    logger_config.init_logger()
    logger.info("Service started.")

    # processing_spreadsheets_with_file()
    processing_spreadsheets_with_parsing()


@logger.catch
def processing_spreadsheets_with_parsing():
    import modules.excel_parser as excel_parser

    paths = [
        "example/data/excel/bachelor/RPND-bachelor.xlsx",
        "example/data/excel/magistracy/RPND-magistracy.xlsx"
    ]

    for path in paths:
        spreadsheets_data, errors = excel_parser.processing_of_spreadsheet(path)
        logger.debug(f"{errors=}")

        excel_parser.processing_spreadsheet_data(spreadsheets_data)
        logger.success(f"File {path} processed")


@logger.catch
def processing_spreadsheets_with_file():
    import json
    import modules.excel_parser as excel_parser

    json_file_path = "/home/oleksandrix/Projects/Python/LdsExcelParser/example/example.json"

    with open(json_file_path, "r", encoding="utf-8") as file:
        spreadsheets_data = json.load(file)
        excel_parser.processing_spreadsheet_data(spreadsheets_data)


if __name__ == "__main__":
    main()
