from pydantic import BaseModel
from src.dto.base_dto import IdMixinSchema, TimestampMixinSchema


class DepartmentSchema(IdMixinSchema, TimestampMixinSchema):
    department_code: int = None
    department_name: str = None


class DepartmentCreateSchema(BaseModel):
    department_code: int
    department_name: str
