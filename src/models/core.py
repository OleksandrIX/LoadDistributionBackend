import uuid
from sqlalchemy import Column, UUID, TIMESTAMP, func
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class IdMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


@declarative_mixin
class TimestampMixin:
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
