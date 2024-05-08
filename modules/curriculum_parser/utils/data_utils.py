PARTITION_VALUE = "ВІЙСЬКОВИЙ  ІНСТИТУТ  ТЕЛЕКОМУНІКАЦІЙ  ТА  ІНФОРМАТИЗАЦІЇ  імені  ГЕРОЇВ  КРУТ"

"""Map for table column names"""
TABLE_COLUMNS: dict = {
    2: "education_component_code",
    3: "education_component_name",
    4: "department",
    5: "credits",
    6: "hours",
    (7, 19): "total_amount_hours",
    (8, 20): "amount_classroom_hours",
    (9, 21): "lecture_hours",
    (10, 22): "group_hours",
    (11, 23): "practical_hours",
    (12, 24): "self_study_hours",
    (13, 25): "term_papers",
    (14, 26): "modular_control_works",
    (15, 27): "calculation_graphic_works",
    (16, 28): "essays",
    (17, 29): "exam",
    (18, 30): "graded_test",
}

"""Map for reporiting types"""
REPORTING_TYPES: dict = {
    "exam": "Екзамен",
    "graded_test": "Диференційований залік"
}


def get_column_name_by_number(column_number: int) -> str | None:
    """Get column name by number column."""
    for key, value in TABLE_COLUMNS.items():
        if isinstance(key, int) and key == column_number:
            return value
        elif isinstance(key, tuple) and column_number in key:
            return value
    return None


def get_semester_number_by_column(column_number: int) -> int | None:
    """
    Get semester number by column number. \n
    For columns with number in the range of 7 to 18, this is the semester number 1. \n
    For columns with number in the range of 19 to 30, this is the semester number 2. \n
    """
    semester_column_number_range = [(7, 18), (19, 30)]
    for i, (start, end) in enumerate(semester_column_number_range):
        if start <= column_number <= end:
            return i + 1
    return None
