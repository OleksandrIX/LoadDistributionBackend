from pydantic import BaseModel, Field

from ..utils.schema import IdMixinSchema, TimestampMixinSchema


class AcademicTaskBase(BaseModel):
    term_papers: int = Field(..., ge=0, le=10)
    modular_control_works: int = Field(..., ge=0, le=10)
    essays: int = Field(..., ge=0, le=10)
    calculation_graphic_works: int = Field(..., ge=0, le=10)
    semester_id: str


class AcademicTaskCreateSchema(AcademicTaskBase):
    ...


class AcademicTaskUpdateSchema(AcademicTaskBase):
    ...


class AcademicTaskSchema(TimestampMixinSchema, IdMixinSchema, AcademicTaskBase):
    ...
