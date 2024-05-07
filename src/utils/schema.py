from uuid import UUID
from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class IdMixinSchema(BaseModel):
    id: UUID


class TimestampMixinSchema(BaseModel):
    created_at: datetime
    updated_at: datetime


class EducationDegreeEnum(str, Enum):
    bachelor = "bachelor"
    master = "master"


class ReportingTypeEnum(str, Enum):
    graded_test = "graded_test"
    exam = "exam"
