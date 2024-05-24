from sqlalchemy import Column, SmallInteger, UUID, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from ..schemas import AcademicTaskSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class AcademicTaskModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "academic_tasks"

    term_papers = Column(SmallInteger, nullable=False)
    modular_control_works = Column(SmallInteger, nullable=False)
    essays = Column(SmallInteger, nullable=False)
    calculation_graphic_works = Column(SmallInteger, nullable=False)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id"), nullable=False)

    semester = relationship("SemesterModel", back_populates="academic_task", uselist=False)

    __table_args__ = (
        CheckConstraint("0 <= term_papers <= 10"),
        CheckConstraint("0 <= modular_control_works <= 10"),
        CheckConstraint("0 <= essays <= 10"),
        CheckConstraint("0 <= calculation_graphic_works <= 10")
    )

    def to_read_model(self) -> AcademicTaskSchema:
        return AcademicTaskSchema.from_orm(self)
