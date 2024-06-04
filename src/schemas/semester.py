from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .academic_hours import AcademicHoursSchema
from .academic_task import AcademicTaskSchema
from ..utils.schema import IdMixinSchema, TimestampMixinSchema, ReportingTypeEnum


class SemesterBase(BaseModel):
    semester_number: int = Field(..., ge=1, le=8)
    total_amount_hours: int = Field(..., ge=0, le=1000)
    reporting_type: Optional[ReportingTypeEnum] = None
    education_component_id: UUID


class SemesterCreateSchema(SemesterBase):
    ...


class SemesterUpdateSchema(SemesterBase):
    ...


class SemesterSchema(TimestampMixinSchema, IdMixinSchema, SemesterBase):
    class Config:
        from_attributes = True


class SemesterWithAcademicDataSchema(SemesterSchema):
    academic_hours: AcademicHoursSchema
    academic_task: AcademicTaskSchema
