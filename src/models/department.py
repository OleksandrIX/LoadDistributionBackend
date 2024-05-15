from sqlalchemy import Column, String, SmallInteger, CheckConstraint
from sqlalchemy.orm import relationship

from ..schemas import DepartmentSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class DepartmentModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "departments"

    department_code = Column(SmallInteger, nullable=False, unique=True)
    department_name = Column(String(255), nullable=False, unique=True)

    specialties = relationship("SpecialtyModel", back_populates="department")
    education_components = relationship("EducationComponentModel", back_populates="department")
    teachers = relationship("TeacherModel", back_populates="department")

    __table_args__ = (CheckConstraint("department_code >= 1 and department_code <= 99"),)

    def to_read_model(self) -> DepartmentSchema:
        return DepartmentSchema(
            id=self.id,
            department_code=self.department_code,
            department_name=self.department_name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
