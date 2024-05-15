from sqlalchemy import Column, String
from sqlalchemy import Column, String, Enum, UUID, ForeignKey

from ..schemas import UserSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class UserModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "users"

    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))

    department = relationship("DepartmentModel", back_populates="users")

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            department_id=str(self.department_id),
            created_at=self.created_at,
            updated_at=self.updated_at
        )
