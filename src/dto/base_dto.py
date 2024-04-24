from datetime import datetime
from uuid import UUID as uuid_type
from pydantic import BaseModel


class IdMixinSchema(BaseModel):
    id: uuid_type = None


class TimestampMixinSchema(BaseModel):
    created_at: datetime = None
    updated_at: datetime = None


