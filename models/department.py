import uuid
import datetime
from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self, id, created_at, updated_at):
        self.id = id or uuid.uuid4()
        self.created_at = created_at or datetime.datetime.now()
        self.updated_at = updated_at or datetime.datetime.now()

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def from_dict(self):
        pass


class Department(Entity):
    def __init__(self, id, created_at, updated_at, department_code, department_name, specialization):
        super().__init__(id, created_at, updated_at)
        self.department_code = department_code
        self.department_name = department_name
        self.specialization = specialization

    def to_dict(self):
        return {
            "id": self.id,
            "department_code": self.department_code,
            "department_name": self.department_name,
            "specialization": self.specialization,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, department_dict: dict):
        if department_dict is None:
            return cls()
        return cls(**department_dict)
