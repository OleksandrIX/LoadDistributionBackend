class ConflictException(Exception):
    def __init__(self, message=None):
        self.status_code = 409
        self.message = message or "Conflict"


class DepartmentConflictException(ConflictException):
    def __init__(self):
        super().__init__(message="Department with such data already exists")


class SpecialtyConflictException(ConflictException):
    def __init__(self):
        super().__init__(message="Specialty with such data already exists")


class SpecializationConflictException(ConflictException):
    def __init__(self):
        super().__init__(message="Specialization with such data already exists")


class EducationComponentConflictException(ConflictException):
    def __init__(self):
        super().__init__(message="Education component with such data already exists")


class StudyGroupConflictException(ConflictException):
    def __init__(self):
        super().__init__(message="Study group with such data already exists")


class SemesterConflictException(ConflictException):
    def __init__(self):
        super().__init__(message="Semester with such data already exists")


class AcademicHoursConflictException(ConflictException):
    def __init__(self):
        super().__init__(message="Academic hours with such data already exists")


class AcademicTaskConflictException(ConflictException):
    def __init__(self):
        super().__init__(message="Academic task with such data already exists")


class UserConflictException(ConflictException):
    def __init__(self, message=None):
        super().__init__(message=message or "User with such data already exists")


class TeacherConflictException(ConflictException):
    def __init__(self, message=None):
        super().__init__(message=message or "Teacher with such data already exists")
