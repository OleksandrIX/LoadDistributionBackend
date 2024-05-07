from sqlalchemy import Column, UUID, SmallInteger, Enum, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from ..schemas import SemesterSchema
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

    def to_read_model(self) -> SemesterSchema:
        return SemesterSchema(
            id=self.id,
            semester_number=self.semester_number,
            total_amount_hours=self.total_amount_hours,
            reporting_type=self.reporting_type,
            education_component_id=str(self.education_component_id),
            created_at=self.created_at,
            updated_at=self.updated_at
        )
