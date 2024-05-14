from sqlalchemy import Column, String

from ..schemas import UserSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class UserModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "users"

    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
