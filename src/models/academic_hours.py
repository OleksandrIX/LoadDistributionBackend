from sqlalchemy import Column, SmallInteger, UUID, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from ..utils.database import Base
from .core import IdMixin, TimestampMixin


class AcademicHoursModel(Base, IdMixin, TimestampMixin):
    __tablename__ = "academic_hours"

    amount_classroom_hours = Column(SmallInteger, nullable=False)
    lecture_hours = Column(SmallInteger, nullable=False)
    group_hours = Column(SmallInteger, nullable=False)
    practical_hours = Column(SmallInteger, nullable=False)
    self_study_hours = Column(SmallInteger, nullable=False)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id"), nullable=False)

    semester = relationship("SemesterModel", back_populates="academic_hours", uselist=False)

    __table_args__ = (
        CheckConstraint("0 <= amount_classroom_hours <= 1200"),
        CheckConstraint("0 <= lecture_hours <= 400"),
        CheckConstraint("0 <= group_hours <= 400"),
        CheckConstraint("0 <= practical_hours <= 400"),
        CheckConstraint("0 <= self_study_hours <= 400"),
    )
