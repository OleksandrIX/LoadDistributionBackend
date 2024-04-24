from sqlalchemy import Column, String, SmallInteger, CheckConstraint
from sqlalchemy.orm import relationship

from ..utils.database import Base
from .core import IdMixin, TimestampMixin


class DepartmentModel(Base, IdMixin, TimestampMixin):
    __tablename__ = "departments"

    department_code = Column(SmallInteger, nullable=False, unique=True)
    department_name = Column(String(255), nullable=False, unique=True)

    specialties = relationship("SpecialtyModel", back_populates="department")
    education_components = relationship("EducationComponentModel", back_populates="department")

    __table_args__ = (CheckConstraint("department_code >= 1 and department_code <= 99"),)
