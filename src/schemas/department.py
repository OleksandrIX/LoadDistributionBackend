from pydantic import BaseModel, Field

from ..utils.schema import IdMixinSchema, TimestampMixinSchema
from .teacher import TeacherSchema


class DepartmentBase(BaseModel):
    department_code: int = Field(..., ge=1, le=99)
    department_name: str = Field(..., max_length=255)


class DepartmentCreateSchema(DepartmentBase):
    ...


class DepartmentUpdateSchema(DepartmentBase):
    ...


class DepartmentSchema(TimestampMixinSchema, IdMixinSchema, DepartmentBase):
    class Config:
        from_attributes = True


class DepartmentWithTeachersSchema(DepartmentSchema):
    teachers: list[TeacherSchema]
