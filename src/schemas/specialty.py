from uuid import UUID

from pydantic import BaseModel, Field

from ..utils.schema import IdMixinSchema, TimestampMixinSchema


class SpecialtyBase(BaseModel):
    specialty_code: str = Field(..., max_length=20)
    specialty_name: str = Field(..., max_length=255)
    department_id: UUID


class SpecialtyCreateSchema(SpecialtyBase):
    ...


class SpecialtyUpdateSchema(SpecialtyBase):
    ...


class SpecialtySchema(TimestampMixinSchema, IdMixinSchema, SpecialtyBase):
    class Config:
        from_attributes = True
