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


class EducationComponentConflictException(ConflictException):
    def __init__(self):
        super().__init__(massage="Education component with such data already exists")


class StudyGroupConflictException(ConflictException):
    def __init__(self):
        super().__init__(massage="Study group with such data already exists")


class SemesterConflictException(ConflictException):
    def __init__(self):
        super().__init__(massage="Semester with such data already exists")


class AcademicHoursConflictException(ConflictException):
    def __init__(self):
        super().__init__(massage="Academic hours with such data already exists")


class AcademicTaskConflictException(ConflictException):
    def __init__(self):
        super().__init__(massage="Academic task with such data already exists")


class UserConflictException(ConflictException):
    def __init__(self, message=None):
        super().__init__(massage=message or "User with such data already exists")
