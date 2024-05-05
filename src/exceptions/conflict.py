class ConflictException(Exception):
    def __init__(self, massage=None):
        self.status_code = 409
        self.massage = massage or "Conflict"


class DepartmentConflictException(ConflictException):
    def __init__(self):
        super().__init__(massage="Department with such data already exists")
