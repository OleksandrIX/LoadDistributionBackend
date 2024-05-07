from pydantic import BaseModel, Field

from ..utils.schema import IdMixinSchema, TimestampMixinSchema, EducationDegreeEnum


class EducationComponentBase(BaseModel):
    education_component_name: str = Field(..., max_length=255)
    education_component_code: str = Field(..., max_length=30)
    education_degree: EducationDegreeEnum
    credits: int = Field(..., gt=0, le=100)
    hours: int = Field(..., ge=1, le=1000)


class EducationComponentCreateSchema(EducationComponentBase):
    ...


class EducationComponentUpdateSchema(EducationComponentBase):
    ...


class EducationComponentSchema(TimestampMixinSchema, IdMixinSchema, EducationComponentBase):
    ...
