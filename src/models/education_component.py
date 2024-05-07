from sqlalchemy import Column, Enum, String, Numeric, SmallInteger, UUID, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship

from .many_to_many_tables import education_components_study_groups
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class EducationComponentModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "education_components"

    education_component_name = Column(String(255), nullable=False)
    education_component_code = Column(String(30), nullable=False)
    education_degree = Column(Enum("bachelor", "master",
                                   name="education_degree_enum",
                                   schema="load_distribution"), nullable=False)
    credits = Column(Numeric(5, 2), nullable=False)
    hours = Column(SmallInteger, nullable=False)

    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)
    specialization_id = Column(UUID(as_uuid=True), ForeignKey("specializations.id"), nullable=False)

    department = relationship("DepartmentModel", back_populates="education_components")
    specialization = relationship("SpecializationModel", back_populates="education_components")

    semesters = relationship("SemesterModel", back_populates="education_component")

    study_groups = relationship("StudyGroupModel",
                                education_components_study_groups,
                                back_populates="education_components",
                                lazy="selectin")

    __table_args__ = (
        UniqueConstraint("education_component_code", "education_degree", name="ec_unique_combination"),
        CheckConstraint("0.01 <= credits <= 100.00"),
        CheckConstraint("1 <= hours <= 1000")
    )
