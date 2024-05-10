from pydantic import BaseModel


class TokenPayloadSchema(BaseModel):
    sub: str
    exp: int


class TokenSchema(BaseModel):
    access_token: str
