from sqlalchemy import Column, String, UUID, ForeignKey, SmallInteger, Numeric
from sqlalchemy.orm import relationship

from ..schemas import DisciplineWithRelationships
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class DisciplineModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "disciplines"

    discipline_name = Column(String, nullable=False, unique=True)
    credits = Column(Numeric(5, 2), nullable=False)
    hours = Column(SmallInteger, nullable=False)

    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)

    department = relationship(
        argument="DepartmentModel",
        back_populates="disciplines",
        lazy="selectin"
    )

    education_components = relationship(
        argument="EducationComponentModel",
        back_populates="discipline",
        lazy="selectin"
    )

    academic_workloads = relationship(
        argument="AcademicWorkloadModel",
        back_populates="discipline",
        lazy="selectin"
    )

    def to_read_model(self) -> DisciplineWithRelationships:
        return DisciplineWithRelationships.from_orm(self)
