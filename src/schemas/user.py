from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from ..utils.schema import IdMixinSchema, TimestampMixinSchema, RoleEnum


class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=30)
    password: str = Field(..., min_length=8, max_length=32)


class UserRegistrationSchema(BaseModel):
    username: str = Field(..., max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)


class UserBase(BaseModel):
    username: str = Field(..., max_length=30)
    email: EmailStr
    role: RoleEnum
    department_id: Optional[UUID]


class UserSchema(TimestampMixinSchema, IdMixinSchema, UserBase):
    password: str

    class Config:
        from_attributes = True


class UserWithoutPasswordSchema(TimestampMixinSchema, IdMixinSchema, UserBase):
    ...
