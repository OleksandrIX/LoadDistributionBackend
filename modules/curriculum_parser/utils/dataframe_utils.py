import io
import pandas as pd

from .spreadsheet_utils import get_indexes_from_cell_range
from ..exceptions import ParsingException


def get_data_frame_from_cell_range(file: io.FileIO, sheet_name: str, cell_range: str) -> pd.DataFrame:
    """Get data frame from Excel sheet with given sheet name and cell range."""
    column_start, row_start, column_end, row_end = get_indexes_from_cell_range(cell_range)

    block_df = pd.read_excel(file,
                             sheet_name=sheet_name,
                             header=None,
                             usecols=f"{column_start}:{column_end}",
                             skiprows=row_start - 1,
                             nrows=row_end - row_start + 1)

    return block_df


def get_table_data_frame_from_block(block_df: pd.DataFrame) -> pd.DataFrame:
    """Get table data frame from block data frame"""
    found_row = None
    for index, row in block_df.iterrows():
        values = set(row.values)
        if all(i in values for i in range(1, 31)):
            found_row = index
            break

    if found_row is None:
        raise ParsingException("В таблиці не знайдено рядка з назвами колонок(графів)")

    table_df = block_df.iloc[found_row:-1, 1:]
    return table_df
