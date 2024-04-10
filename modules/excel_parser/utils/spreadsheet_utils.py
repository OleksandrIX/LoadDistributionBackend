from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.read_only import ReadOnlyCell
from modules.excel_parser.utils.data_utils import *


def get_column_index(cell_name: str) -> str:
    """
    Get column index from cell name. \n
    Example: cell_name="A1" -> column_index="A"
    """
    return "".join(filter(str.isalpha, cell_name))


def get_row_index(cell_name: str) -> int:
    """
    Get row index from cell name. \n
    Example: cell_name="A1" -> column_index="1"
    """
    return int("".join(filter(str.isdigit, cell_name)))


def get_start_and_end_cell_from_cell_range(cell_range: str) -> tuple[str, str]:
    """
    Get start and end cell from cell range. \n
    Example: cell_range="A1:BH16" -> (start_cell="A1", end_cell="BH16")
    """
    start_cell, end_cell = cell_range.split(":")
    return start_cell, end_cell


def get_indexes_from_cell_range(cell_range: str) -> tuple[str, int, str, int]:
    """
    Get indexes from cell range. \n
    Example: cell_range="A1:BH16" -> (column_start="A", row_start=1, column_end="BH", row_end=16)
    """
    start_cell, end_cell = get_start_and_end_cell_from_cell_range(cell_range)
    row_start: int = get_row_index(start_cell)
    row_end: int = get_row_index(end_cell)
    column_start: str = get_column_index(start_cell)
    column_end: str = get_column_index(end_cell)
    return column_start, row_start, column_end, row_end


def check_border_in_cell(cell: ReadOnlyCell) -> bool:
    """Checks if the cell has top and bottom border"""
    if not cell:
        return False
    if not cell.border:
        return False
    if cell.border.top.style is None and cell.border.bottom.style is None:
        return False
    return True


def check_border_in_row(row: tuple[ReadOnlyCell, ...]) -> bool:
    """Checks if the entire row has top and bottom border"""
    for cell in row:
        if not check_border_in_cell(cell):
            return False
    return True


def get_start_and_end_row_for_table(block: Worksheet, start_row: int) -> tuple[int, int]:
    """Returns the start and end row number for the given worksheet block within the given worksheet."""
    start_table_row = None
    end_table_row = None

    for row_idx, row in enumerate(block, start=1):
        if check_border_in_row(row):
            if start_table_row is None:
                start_table_row = row_idx
            end_table_row = row_idx

    return start_table_row + start_row, end_table_row + start_row


def get_indexes_and_blocks_from_worksheet(worksheet: Worksheet, start_cell: str, end_cell: str) -> tuple[list[int], list[str]]:
    """Returns the tuple with arrays indexes and blocks ranges for the given worksheet"""
    row_end = get_row_index(end_cell)
    column_start = get_column_index(start_cell)
    column_end = get_column_index(end_cell)

    indexes = [int(get_row_index(cell.coordinate)) - 1
               for row in worksheet.rows
               for cell in row
               if [value.lower() for value in str(cell.value).split()]
               == [value.lower() for value in PARTITION_VALUE.split()]]
    indexes.append(row_end)

    blocks = [f"{column_start}{indexes[i] + 1}:{column_end}{indexes[i + 1]}"
              for i in range(len(indexes)) if i + 1 < len(indexes)]

    return indexes, blocks


def get_subblocks_from_block(worksheet: Worksheet, block: str, start_row_for_block: int) -> tuple[str, str, str]:
    """
    Takes a range of block cells and the starting row number, and returns a tuple: \n
    - range of cells for the block header, \n
    - range of cells for the table, \n
    - range of cells for block footer.
    """
    worksheet_block: Worksheet = worksheet[block]
    start_row_for_table, end_row_for_table = get_start_and_end_row_for_table(worksheet_block, start_row_for_block)

    start_row_for_footer = end_row_for_table + 1
    end_row_for_header = start_row_for_table - 1

    column_start, row_start, column_end, row_end = get_indexes_from_cell_range(block)

    header_block = f"{column_start}{row_start}:{column_end}{end_row_for_header}"
    table_block = f"{column_start}{start_row_for_table}:{column_end}{end_row_for_table}"
    footer_block = f"{column_start}{start_row_for_footer}:{column_end}{row_end}"

    return header_block, table_block, footer_block
