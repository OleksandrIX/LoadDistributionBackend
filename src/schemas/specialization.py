from pydantic import BaseModel, Field

from ..utils.schema import IdMixinSchema, TimestampMixinSchema


class SpecializationBase(BaseModel):
    specialization_code: str = Field(..., max_length=20)
    specialization_name: str = Field(..., max_length=255)
    specialty_id: str


class SpecializationCreateSchema(SpecializationBase):
    ...


class SpecializationUpdateSchema(SpecializationBase):
    ...


class SpecializationSchema(TimestampMixinSchema, IdMixinSchema, SpecializationBase):
    ...
