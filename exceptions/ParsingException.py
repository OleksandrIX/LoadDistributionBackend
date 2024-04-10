class ParsingException(Exception):
    def __init__(self,
                 message,
                 sheet_name=None,
                 block=None,
                 row=None,
                 column=None):
        super().__init__(message)
        self.sheet_name = sheet_name
        self.block = block
        self.row = row
        self.column = column

    def __str__(self):
        error_str = f"{self.args[0]}"
        if self.block is not None:
            error_str += f". Блок: {self.block}"
        if self.sheet_name is not None:
            error_str += f". Аркуш: {self.sheet_name}"
        if self.row is not None and self.column is not None:
            error_str += f". Рядок: {self.row}, Колонка: {self.column}"
        return error_str
