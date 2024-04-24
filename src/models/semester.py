from sqlalchemy import Column, UUID, SmallInteger, Enum, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from ..utils.database import Base
from .core import IdMixin, TimestampMixin


class SemesterModel(Base, IdMixin, TimestampMixin):
    __tablename__ = "semesters"

    semester_number = Column(SmallInteger, nullable=False)
    total_amount_hours = Column(SmallInteger, nullable=False)
    reporting_type = Column(Enum("exam", "graded_test"), nullable=False)
    education_component_id = Column(UUID(as_uuid=True), ForeignKey("education_components.id"), nullable=False)

    education_component = relationship("EducationComponentModel", back_populates="semesters")
    academic_hours = relationship("AcademicHoursModel", back_populates="semester", uselist=False)
    academic_task = relationship("AcademicTaskModel", back_populates="semester", uselist=False)

    __table_args__ = (
        CheckConstraint("1 <= semester_number <= 8"),
        CheckConstraint("0 <= total_amount_hours <= 1000")
    )
