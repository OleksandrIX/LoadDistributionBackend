import uuid
import datetime
from abc import ABC, abstractmethod


class BaseEntity(ABC):
    def __init__(self, id, created_at, updated_at):
        self.id = id or uuid.uuid4()
        self.created_at = created_at or datetime.datetime.now()
        self.updated_at = updated_at or datetime.datetime.now()

    @abstractmethod
    def to_dict(self):
        pass

    @staticmethod
    def from_tuple(cls, object_tuple: tuple):
        if object_tuple is None:
            return cls()
        return cls(*object_tuple)

    @staticmethod
    def from_dict(cls, object_dict: dict):
        if object_dict is None:
            return cls()
        return cls(**object_dict)
