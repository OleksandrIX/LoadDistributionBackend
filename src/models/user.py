from sqlalchemy import Column, String, Enum, UUID, ForeignKey
from sqlalchemy.orm import relationship

from ..schemas import UserSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin, role_enum_args


class UserModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "users"

    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(Enum(*role_enum_args,
                       name="role_enum",
                       schema="load_distribution"), nullable=False)

    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))

    department = relationship("DepartmentModel", back_populates="users")

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            role=self.role,
            department_id=str(self.department_id),
            created_at=self.created_at,
            updated_at=self.updated_at
        )
