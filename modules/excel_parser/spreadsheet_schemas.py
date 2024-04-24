from enum import Enum
from typing import Optional
from pydantic import BaseModel


class EducationDegreeEnum(str, Enum):
    """Enumeration of possible Education Degree (bachelor and master education degree)"""
    bachelor = "бакалавр"
    master = "магістр"


class ReportingTypeEnum(str, Enum):
    """Enumeration of possible ReportingType (graded_test and exam)"""
    graded_test = "Диференційований залік"
    exam = "Екзамен"


class SpreadsheetBlockSchema(BaseModel):
    """Schema for data from spreadsheet block"""
    specialty_code: int
    specialization_name: str
    course_study: int
    education_degree: EducationDegreeEnum
    study_groups: list[tuple[int, int]] = []


class AcademicHoursSchema(BaseModel):
    """Schema for data from academic hours"""
    amount_classroom_hours: int
    lecture_hours: int
    group_hours: int
    practical_hours: int
    self_study_hours: int


class AcademicTasksSchema(BaseModel):
    """Schema for data from academic task"""
    term_papers: int
    modular_control_works: int
    calculation_graphic_works: int
    essays: int


class SemesterSchema(BaseModel):
    """Schema for data from semester"""
    semester_number: int
    total_amount_hours: int
    academic_hours: AcademicHoursSchema
    academic_task: AcademicTasksSchema
    reporting_type: Optional[ReportingTypeEnum] = None


class EducationComponentSchema(BaseModel):
    """Schema for data from education component"""
    education_component_code: str
    education_component_name: str
    department: int
    credits: float
    hours: int
    semesters: list[SemesterSchema]
