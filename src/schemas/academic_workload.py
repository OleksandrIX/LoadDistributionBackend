from uuid import UUID

from pydantic import BaseModel, Field

from ..utils.schema import IdMixinSchema, TimestampMixinSchema


class AcademicWorkloadBase(BaseModel):
    lecture_hours: int = Field(0, ge=0, le=10000)
    group_hours: int = Field(0, ge=0, le=10000)
    practical_hours: int = Field(0, ge=0, le=10000)
    laboratory_reports_checking_hours: float = Field(0.0, ge=0.0, le=10000.0)
    special_exercises_conducting_hours: float = Field(0.0, ge=0.0, le=10000.0)
    consultation_hours: float = Field(0.0, ge=0.0, le=10000.0)
    term_papers_conducting_hours: float = Field(0.0, ge=0.0, le=10000.0)
    control_works_checking_hours: float = Field(0.0, ge=0.0, le=10000.0)
    graded_tests_conducting_hours: float = Field(0.0, ge=0.0, le=10000.0)
    exams_conducting_hours: float = Field(0.0, ge=0.0, le=10000.0)
    military_internship_conducting_hours: float = Field(0.0, ge=0.0, le=10000.0)
    supervision_qualification_works_hours: float = Field(0.0, ge=0.0, le=10000.0)
    qualification_works_defense_conducting_hours: float = Field(0.0, ge=0.0, le=10000.0)
    complex_exams_conducting_hours: float = Field(0.0, ge=0.0, le=10000.0)
    other_types_conducting_hours: float = Field(0.0, ge=0.0, le=10000.0)
    discipline_id: UUID = Field(...)


class AcademicWorkloadCreateSchema(AcademicWorkloadBase):
    ...


class AcademicWorkloadUpdateSchema(AcademicWorkloadBase):
    ...


class AcademicWorkloadSchema(TimestampMixinSchema, IdMixinSchema, AcademicWorkloadBase):
    class Config:
        from_attributes = True
