class NotFoundException(Exception):
    def __init__(self, massage=None):
        self.status_code = 404
        self.massage = massage or "Not Found"


class DepartmentNotFoundException(NotFoundException):
    def __init__(self, department_id):
        massage = f"Department with id '{department_id}' not found"
        super().__init__(massage=massage)
