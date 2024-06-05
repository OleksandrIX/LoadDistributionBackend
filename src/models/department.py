from sqlalchemy import Column, String, SmallInteger, CheckConstraint
from sqlalchemy.orm import relationship

from ..schemas import (DepartmentSchema,
                       DepartmentWithTeachersSchema,
                       DepartmentWithDisciplines,
                       DepartmentWithRelationships)
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class DepartmentModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "departments"

    department_code = Column(SmallInteger, nullable=False, unique=True)
    department_name = Column(String(255), nullable=False, unique=True)

    specialties = relationship("SpecialtyModel", back_populates="department", lazy="selectin")
    disciplines = relationship("DisciplineModel", back_populates="department", lazy="selectin")
    teachers = relationship("TeacherModel", back_populates="department", lazy="selectin")
    users = relationship("UserModel", back_populates="department", lazy="selectin")

    __table_args__ = (CheckConstraint("department_code >= 1 and department_code <= 99"),)

    def to_read_model(self) -> DepartmentSchema:
        return DepartmentSchema.from_orm(self)

    def to_read_model_with_teachers(self) -> DepartmentWithTeachersSchema:
        return DepartmentWithTeachersSchema.from_orm(self)

    def to_read_model_with_disciplines(self) -> DepartmentWithDisciplines:
        return DepartmentWithDisciplines.from_orm(self)

    def to_read_model_with_relationships(self) -> DepartmentWithRelationships:
        return DepartmentWithRelationships.from_orm(self)
