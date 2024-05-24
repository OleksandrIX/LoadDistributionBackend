from uuid import UUID

from pydantic import BaseModel, Field

from ..utils.schema import IdMixinSchema, TimestampMixinSchema


class AcademicWorkloadBase(BaseModel):
    lecture_hours: int = Field(..., ge=0, le=1000)
    group_hours: int = Field(..., ge=0, le=1000)
    practical_hours: int = Field(..., ge=0, le=1000)
    laboratory_reports_checking_hours: float = Field(..., ge=0.0, le=1000.0)
    special_exercises_conducting_hours: float = Field(..., ge=0.0, le=1000.0)
    consultation_hours: float = Field(..., ge=0.0, le=1000.0)
    term_papers_conducting_hours: float = Field(..., ge=0.0, le=1000.0)
    control_works_checking_hours: float = Field(..., ge=0.0, le=1000.0)
    graded_tests_conducting_hours: float = Field(..., ge=0.0, le=1000.0)
    exams_conducting_hours: float = Field(..., ge=0.0, le=1000.0)
    military_internship_conducting_hours: float = Field(..., ge=0.0, le=1000.0)
    supervision_qualification_works_hours: float = Field(..., ge=0.0, le=1000.0)
    qualification_works_defense_conducting_hours: float = Field(..., ge=0.0, le=1000.0)
    complex_exams_conducting_hours: float = Field(..., ge=0.0, le=1000.0)
    other_types_conducting_hours: float = Field(..., ge=0.0, le=1000.0)
    education_component_id: UUID
    teacher_id: UUID


class AcademicWorkloadCreateSchema(AcademicWorkloadBase):
    ...


class AcademicWorkloadUpdateSchema(AcademicWorkloadBase):
    ...


class AcademicWorkloadSchema(TimestampMixinSchema, IdMixinSchema, AcademicWorkloadBase):
    class Config:
        from_attributes = True
