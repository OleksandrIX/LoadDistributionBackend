from sqlalchemy import Column, Enum, String, Numeric, SmallInteger, UUID, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship

from .many_to_many_tables import EducationComponentsStudyGroupsModel

from ..schemas import EducationComponentSchema, EducationComponenWithWorkloadSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin, education_degree_enum_agrs


class EducationComponentModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "education_components"

    education_component_name = Column(String(255), nullable=False)
    education_component_code = Column(String(30), nullable=False)
    education_degree = Column(Enum(*education_degree_enum_agrs,
                                   name="education_degree_enum",
                                   schema="load_distribution"), nullable=False)
    credits = Column(Numeric(5, 2), nullable=False)
    hours = Column(SmallInteger, nullable=False)
    numbers_of_flows = Column(SmallInteger, nullable=False, default=0)

    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)
    specialization_id = Column(UUID(as_uuid=True), ForeignKey("specializations.id"), nullable=False)

    department = relationship(
        argument="DepartmentModel",
        back_populates="education_components",
        lazy="selectin"
    )

    specialization = relationship(
        argument="SpecializationModel",
        back_populates="education_components",
        lazy="selectin"
    )

    semesters = relationship(
        argument="SemesterModel",
        back_populates="education_component",
        lazy="selectin"
    )

    academic_workloads = relationship(
        argument="AcademicWorkloadModel",
        back_populates="education_component",
        lazy="selectin"
    )

    study_groups = relationship(
        argument="StudyGroupModel",
        secondary=EducationComponentsStudyGroupsModel.__table__,
        back_populates="education_components",
        lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint("education_component_code", "education_degree", name="ec_unique_combination"),
        CheckConstraint("0.01 <= credits <= 100.00"),
        CheckConstraint("1 <= hours <= 1000")
    )

    def to_read_model(self) -> EducationComponentSchema:
        return EducationComponentSchema.from_orm(self)

    def to_read_model_with_workload(self) -> EducationComponenWithWorkloadSchema:
        return EducationComponenWithWorkloadSchema.from_orm(self)
