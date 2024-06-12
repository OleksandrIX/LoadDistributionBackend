from sqlalchemy import Column, String, UUID, ForeignKey, SmallInteger, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship

from ..schemas import DisciplineWithRelationships
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class DisciplineModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "disciplines"

    discipline_name = Column(String, nullable=False)
    credits = Column(Numeric(5, 2), nullable=False)
    hours = Column(SmallInteger, nullable=False)
    data_of_years = Column(String(10), nullable=False)

    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    academic_workload_id = Column(UUID(as_uuid=True), ForeignKey("academic_workloads.id", ondelete="CASCADE"), nullable=True)

    department = relationship(
        argument="DepartmentModel",
        back_populates="disciplines",
        lazy="selectin",
    )

    education_components = relationship(
        argument="EducationComponentModel",
        back_populates="discipline",
        lazy="selectin",
    )

    academic_workload = relationship(
        argument="AcademicWorkloadModel",
        back_populates="discipline",
        lazy="selectin",
        uselist=False,
    )

    academic_workload_teacher = relationship(
        argument="AcademicWorkloadTeacherModel",
        back_populates="discipline",
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint(
            "discipline_name",
            "data_of_years",
            "department_id",
            name="discipline_unique_combination"
        ),
    )

    def to_read_model(self) -> DisciplineWithRelationships:
        return DisciplineWithRelationships.from_orm(self)
