from loguru import logger
from pydantic import BaseModel, field_validator

from ..utils.schema import IdMixinSchema, TimestampMixinSchema


class DepartmentBase(BaseModel):
    department_code: int
    department_name: str

    @field_validator("department_code")
    @classmethod
    def validate_department_code(cls, value):
        if value < 1 or value > 99:
            logger.warning("Department code must be between 1 and 99")
            raise ValueError("Department code must be between 1 and 99")
        return value


class DepartmentCreateSchema(DepartmentBase):
    ...


class DepartmentUpdateSchema(DepartmentBase):
    ...


class DepartmentSchema(TimestampMixinSchema, IdMixinSchema, DepartmentBase):
    ...
