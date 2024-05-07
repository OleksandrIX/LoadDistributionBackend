from pydantic import BaseModel, Field

from ..utils.schema import IdMixinSchema, TimestampMixinSchema


class AcademicHoursBase(BaseModel):
    amount_classroom_hours: int = Field(..., ge=0, le=1200)
    lecture_hours: int = Field(..., ge=0, le=400)
    group_hours: int = Field(..., ge=0, le=400)
    practical_hours: int = Field(..., ge=0, le=400)
    self_study_hours: int = Field(..., ge=0, le=400)
    semester_id: str


class AcademicHoursCreateSchema(AcademicHoursBase):
    ...


class AcademicHoursUpdateSchema(AcademicHoursBase):
    ...


class AcademicHoursSchema(TimestampMixinSchema, IdMixinSchema, AcademicHoursBase):
    ...
