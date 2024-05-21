from ..exceptions import ClientException

ALLOWED_CURRICULUM_EXTENSIONS = ["xls", "xlsx", "ods"]


def check_curriculm_file_extension(filename: str) -> None:
    file_extension = filename.split(".")[-1].lower()
    is_allowed_extension = file_extension in ALLOWED_CURRICULUM_EXTENSIONS
    if not is_allowed_extension:
        raise ClientException(message="Неправильний тип файлу. Допускаються лише файли електронних таблиць.")
