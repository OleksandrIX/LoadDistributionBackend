from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class IdMixinSchema(BaseModel):
    id: UUID


class TimestampMixinSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
