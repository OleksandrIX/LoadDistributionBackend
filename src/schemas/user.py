from pydantic import BaseModel, Field, EmailStr

from ..utils.schema import IdMixinSchema, TimestampMixinSchema


class UserBase(BaseModel):
    username: str = Field(..., max_length=30)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserLoginSchema(UserBase):
    password: str = Field(..., min_length=8, max_length=32)


class UserRegistrationSchema(UserBase):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)


class UserSchema(TimestampMixinSchema, IdMixinSchema, UserBase):
    email: EmailStr
    password: str
