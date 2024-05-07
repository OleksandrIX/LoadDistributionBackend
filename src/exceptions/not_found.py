class NotFoundException(Exception):
    def __init__(self, massage=None):
        self.status_code = 404
        self.massage = massage or "Not Found"


class DepartmentNotFoundException(NotFoundException):
    def __init__(self, department_id):
        massage = f"Department with id '{department_id}' not found"
        super().__init__(massage=massage)


class SpecialtyNotFoundException(NotFoundException):
    def __init__(self, specialty_id):
        massage = f"Specialty with id '{specialty_id}' not found"
        super().__init__(massage=massage)


class SpecializationNotFoundException(NotFoundException):
    def __init__(self, specialization_id):
        massage = f"Specialization with id '{specialization_id}' not found"
        super().__init__(massage=massage)


class EducationComponentNotFoundException(NotFoundException):
    def __init__(self, education_component_id):
        massage = f"Education component with id '{education_component_id}' not found"
        super().__init__(massage=massage)
