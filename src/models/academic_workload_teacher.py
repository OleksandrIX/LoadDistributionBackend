from sqlalchemy import Column, ForeignKey, UUID, SmallInteger
from sqlalchemy.orm import relationship

from ..schemas import AcademicWorkloadTeacherSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class AcademicWorkloadTeacherModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "academic_workloads_teachers"

    semester_number = Column(SmallInteger, nullable=False)
    academic_workload_id = Column(UUID(as_uuid=True), ForeignKey("academic_workloads.id", ondelete="CASCADE"), nullable=False)
    discipline_id = Column(UUID(as_uuid=True), ForeignKey("disciplines.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)

    academic_workload = relationship(
        argument="AcademicWorkloadModel",
        back_populates="academic_workload_teacher",
        lazy="selectin"
    )

    discipline = relationship(
        argument="DisciplineModel",
        back_populates="academic_workload_teacher",
        lazy="selectin"
    )

    teacher = relationship(
        argument="TeacherModel",
        back_populates="academic_workloads",
        lazy="selectin"
    )

    def to_read_model(self) -> AcademicWorkloadTeacherSchema:
        return AcademicWorkloadTeacherSchema.from_orm(self)
