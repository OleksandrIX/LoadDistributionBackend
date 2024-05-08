from typing import Optional
from pydantic import BaseModel, Field

from ..utils.schema import IdMixinSchema, TimestampMixinSchema, ReportingTypeEnum


class SemesterBase(BaseModel):
    semester_number: int = Field(..., ge=1, le=8)
    total_amount_hours: int = Field(..., ge=0, le=1000)
    reporting_type: Optional[ReportingTypeEnum] = None
    education_component_id: str


class SemesterCreateSchema(SemesterBase):
    ...


class SemesterUpdateSchema(SemesterBase):
    ...


class SemesterSchema(TimestampMixinSchema, IdMixinSchema, SemesterBase):
    ...
