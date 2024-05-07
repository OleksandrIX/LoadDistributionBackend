class ConflictException(Exception):
    def __init__(self, massage=None):
        self.status_code = 409
        self.massage = massage or "Conflict"


class DepartmentConflictException(ConflictException):
    def __init__(self):
        super().__init__(massage="Department with such data already exists")


class SpecialtyConflictException(ConflictException):
    def __init__(self):
        super().__init__(massage="Specialty with such data already exists")


class SpecializationConflictException(ConflictException):
    def __init__(self):
        super().__init__(massage="Specialization with such data already exists")
