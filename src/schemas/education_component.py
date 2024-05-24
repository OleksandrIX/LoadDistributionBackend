from uuid import UUID

from pydantic import BaseModel, Field

from .academic_workload import AcademicWorkloadSchema
from ..utils.schema import IdMixinSchema, TimestampMixinSchema, EducationDegreeEnum


class EducationComponentBase(BaseModel):
    education_component_name: str = Field(..., max_length=255)
    education_component_code: str = Field(..., max_length=30)
    education_degree: EducationDegreeEnum
    credits: float = Field(..., gt=0, le=100)
    hours: int = Field(..., ge=1, le=1000)
    department_id: UUID
    specialization_id: UUID


class EducationComponentCreateSchema(EducationComponentBase):
    ...


class EducationComponentUpdateSchema(EducationComponentBase):
    ...


class EducationComponentSchema(TimestampMixinSchema, IdMixinSchema, EducationComponentBase):
    class Config:
        from_attributes = True


class EducationComponenWithWorkloadSchema(EducationComponentSchema):
    academic_workloads: list[AcademicWorkloadSchema]
