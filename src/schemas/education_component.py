from uuid import UUID

from pydantic import BaseModel, Field

from .academic_workload import AcademicWorkloadSchema
from .semester import SemesterWithAcademicDataSchema
from .specialization import SpecializationSchema
from .study_group import StudyGroupSchema
from ..utils.schema import IdMixinSchema, TimestampMixinSchema, EducationDegreeEnum


class EducationComponentBase(BaseModel):
    education_component_code: str = Field(..., max_length=30)
    education_degree: EducationDegreeEnum
    course_study: int = Field(..., ge=1, le=10)
    numbers_of_flows: int = Field(0, ge=0, le=50)
    discipline_id: UUID
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


class ECWithAcademicDataSchema(EducationComponentSchema):
    semesters: list[SemesterWithAcademicDataSchema]
    study_groups: list[StudyGroupSchema]


class EducationComponentWithRelationships(EducationComponentSchema):
    specialization: SpecializationSchema
    semesters: list[SemesterWithAcademicDataSchema]
    study_groups: list[StudyGroupSchema]
