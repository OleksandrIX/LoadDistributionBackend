from typing import Optional
from pydantic import BaseModel

from ..utils.schema import EducationDegreeEnum, ReportingTypeEnum


class CurriculumFileSchema(BaseModel):
    bucket_name: str
    filename: str
    content_type: str
    size: int


class CurriculumAcademicHoursSchema(BaseModel):
    amount_classroom_hours: int
    lecture_hours: int
    group_hours: int
    practical_hours: int
    self_study_hours: int


class CurriculumAcademicTasksSchema(BaseModel):
    term_papers: int
    modular_control_works: int
    calculation_graphic_works: int
    essays: int


class CurriculumSemesterSchema(BaseModel):
    semester_number: int
    total_amount_hours: int
    academic_hours: CurriculumAcademicHoursSchema
    academic_task: CurriculumAcademicTasksSchema
    reporting_type: Optional[ReportingTypeEnum] = None


class CurriculumEducationComponentSchema(BaseModel):
    education_component_code: str
    education_component_name: str
    department: int
    credits: float
    hours: int
    semesters: list[CurriculumSemesterSchema]


class CurriculumSpreadsheetBlockBase(BaseModel):
    course_study: int
    education_degree: EducationDegreeEnum
    education_components: list[CurriculumEducationComponentSchema]


class CurriculumSpreadsheetBlockSchema(CurriculumSpreadsheetBlockBase):
    specialization_name: str
    specialty_code: int
    study_groups: list[tuple[int, int]] = []


class CurriculumSpreadsheetBlockRequestSchema(CurriculumSpreadsheetBlockBase):
    specialty: str
    specialization: str
    study_groups: str


class ParsedCurriculumSchema(BaseModel):
    curriculum_file: CurriculumFileSchema
    curriculum_spreadsheet_blocks: list[CurriculumSpreadsheetBlockRequestSchema]
    curriculum_errors: list[tuple[str, str, str]]


class CurriculumDataRequestSchema(BaseModel):
    curriculum_spreadsheet_blocks: list[CurriculumSpreadsheetBlockRequestSchema]


class CurriculumDataSavedResponseSchema(BaseModel):
    education_components: list[str]
