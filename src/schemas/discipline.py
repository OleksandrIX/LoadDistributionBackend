from uuid import UUID

from pydantic import BaseModel, Field

from .education_component import EducationComponentWithRelationships
from .academic_workload import AcademicWorkloadSchema
from ..utils.schema import IdMixinSchema, TimestampMixinSchema


class DisciplineBase(BaseModel):
    discipline_name: str = Field(...)
    credits: float = Field(..., gt=0, le=100)
    hours: int = Field(..., ge=1, le=1000)
    department_id: UUID


class DisciplineCreateSchema(DisciplineBase):
    ...


class DisciplineUpdateSchema(DisciplineBase):
    ...


class DisciplineSchema(TimestampMixinSchema, IdMixinSchema, DisciplineBase):
    class Config:
        from_attributes = True


class DisciplineWithRelationships(DisciplineSchema):
    academic_workloads: list[AcademicWorkloadSchema]
    education_components: list[EducationComponentWithRelationships]
