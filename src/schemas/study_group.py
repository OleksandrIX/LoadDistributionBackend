from pydantic import BaseModel, Field

from ..utils.schema import IdMixinSchema, TimestampMixinSchema, EducationDegreeEnum


class StudyGroupBase(BaseModel):
    group_code: str = Field(..., max_length=10)
    course_study: int = Field(..., ge=1, le=6)
    education_degree: EducationDegreeEnum
    number_listeners: int = Field(..., ge=1, le=50)


class StudyGroupCreateSchema(StudyGroupBase):
    ...


class StudyGroupUpdateSchema(StudyGroupBase):
    ...


class StudyGroupSchema(TimestampMixinSchema, IdMixinSchema, StudyGroupBase):
    ...
