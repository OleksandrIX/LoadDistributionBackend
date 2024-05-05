from sqlalchemy import Column, UUID, SmallInteger, Enum, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class SemesterModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "semesters"

    semester_number = Column(SmallInteger, nullable=False)
    total_amount_hours = Column(SmallInteger, nullable=False)
    reporting_type = Column(Enum("graded_test", "exam",
                                 name="reporting_type_enum",
                                 schema="load_distribution"), nullable=False)
    education_component_id = Column(UUID(as_uuid=True), ForeignKey("education_components.id"), nullable=False)

    education_component = relationship("EducationComponentModel", back_populates="semesters")
    academic_hours = relationship("AcademicHoursModel", back_populates="semester", uselist=False)
    academic_task = relationship("AcademicTaskModel", back_populates="semester", uselist=False)

    __table_args__ = (
        CheckConstraint("1 <= semester_number <= 8"),
        CheckConstraint("0 <= total_amount_hours <= 1000")
    )
