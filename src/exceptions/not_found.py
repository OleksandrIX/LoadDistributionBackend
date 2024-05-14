class NotFoundException(Exception):
    def __init__(self, message=None):
        self.status_code = 404
        self.message = message or "Not Found"


class DepartmentNotFoundException(NotFoundException):
    def __init__(self, department_id):
        message = f"Department with id '{department_id}' not found"
        super().__init__(message=message)


class SpecialtyNotFoundException(NotFoundException):
    def __init__(self, specialty_id):
        message = f"Specialty with id '{specialty_id}' not found"
        super().__init__(message=message)


class SpecializationNotFoundException(NotFoundException):
    def __init__(self, specialization_id):
        message = f"Specialization with id '{specialization_id}' not found"
        super().__init__(message=message)


class EducationComponentNotFoundException(NotFoundException):
    def __init__(self, education_component_id):
        message = f"Education component with id '{education_component_id}' not found"
        super().__init__(message=message)


class StudyGroupNotFoundException(NotFoundException):
    def __init__(self, study_group_id):
        message = f"Study group with id '{study_group_id}' not found"
        super().__init__(message=message)


class SemesterNotFoundException(NotFoundException):
    def __init__(self, semester_id):
        message = f"Semester with id '{semester_id}' not found"
        super().__init__(message=message)


class AcademicHoursNotFoundException(NotFoundException):
    def __init__(self, academic_hours_id):
        message = f"Academic hours with id '{academic_hours_id}' not found"
        super().__init__(message=message)


class AcademicTaskNotFoundException(NotFoundException):
    def __init__(self, academic_task_id):
        message = f"Academic task with id '{academic_task_id}' not found"
        super().__init__(message=message)


class CurriculumNotFoundException(NotFoundException):
    def __init__(self, curriculum_filename):
        message = f"Curriculum file with name '{curriculum_filename}' not found"
        super().__init__(message=message)


class UserByUsernameNotFoundException(NotFoundException):
    def __init__(self, username):
        message = f"User with username '{username}' not found"
        super().__init__(message=message)


class UserByIdNotFoundException(NotFoundException):
    def __init__(self, user_id):
        message = f"User with id '{user_id}' not found"
        super().__init__(message=message)
