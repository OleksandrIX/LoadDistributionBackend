from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .education_component import EducationComponentWithRelationships
from .academic_workload import AcademicWorkloadSchema
from ..utils.schema import IdMixinSchema, TimestampMixinSchema


class DisciplineBase(BaseModel):
    discipline_name: str = Field(...)
    credits: float = Field(..., gt=0, le=100)
    hours: int = Field(..., ge=1, le=1000)
    data_of_years: str = Field(..., max_length=10)
    department_id: UUID = Field(...)
    academic_workload_id: Optional[UUID] = Field(None)


class DisciplineCreateSchema(DisciplineBase):
    ...


class DisciplineUpdateSchema(DisciplineBase):
    ...


class DisciplineSchema(TimestampMixinSchema, IdMixinSchema, DisciplineBase):
    class Config:
        from_attributes = True


class DisciplineWithRelationships(DisciplineSchema):
    academic_workload: Optional[AcademicWorkloadSchema] = Field(None)
    education_components: list[EducationComponentWithRelationships]
