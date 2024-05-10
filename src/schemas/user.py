from pydantic import BaseModel, Field, EmailStr

from ..utils.schema import IdMixinSchema, TimestampMixinSchema


class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=30)
    password: str = Field(..., min_length=8, max_length=32)


class UserRegistrationSchema(BaseModel):
    username: str = Field(..., max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)


class UserSchema(TimestampMixinSchema, IdMixinSchema):
    username: str
    email: EmailStr
    password: str
