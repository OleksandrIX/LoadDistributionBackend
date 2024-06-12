from uuid import UUID

from pydantic import BaseModel, Field

from .teacher import TeacherSchema
from .academic_workload import AcademicWorkloadSchema
from ..utils.schema import IdMixinSchema, TimestampMixinSchema


class AcademicWorkloadTeacherBase(BaseModel):
    semester_number: int = Field(..., ge=1, le=8)
    academic_workload_id: UUID = Field(...)
    discipline_id: UUID = Field(...)
    teacher_id: UUID = Field(...)


class AcademicWorkloadTeacherCreateSchema(AcademicWorkloadTeacherBase):
    ...


class AcademicWorkloadTeacherUpdateSchema   (AcademicWorkloadTeacherBase):
    ...


class AcademicWorkloadTeacherSchema(TimestampMixinSchema, IdMixinSchema, AcademicWorkloadTeacherBase):
    teacher: TeacherSchema
    academic_workload: AcademicWorkloadSchema

    class Config:
        from_attributes = True
