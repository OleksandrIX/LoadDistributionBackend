from models.base_entity import BaseEntity


class Department(BaseEntity):
    def __init__(self, id, department_code, department_name, created_at, updated_at):
        super().__init__(id, created_at, updated_at)
        self.department_code = department_code
        self.department_name = department_name

    def to_dict(self):
        return {
            "id": self.id,
            "department_code": self.department_code,
            "department_name": self.department_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Discipline(BaseEntity):
    def __init__(self, id, discipline_name, credits, hours, department_id, created_at, updated_at):
        super().__init__(id, created_at, updated_at)
        self.discipline_name = discipline_name
        self.credits = credits
        self.hours = hours
        self.department_id = department_id

    def to_dict(self):
        return {
            "id": self.id,
            "discipline_name": self.discipline_name,
            "credits": self.credits,
            "hours": self.hours,
            "department_id": self.department_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
