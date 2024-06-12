from sqlalchemy import (Column, Enum, String, Numeric, SmallInteger, Boolean,
                        CheckConstraint, UUID, ForeignKey, UniqueConstraint)
from sqlalchemy.orm import relationship

from ..schemas import TeacherSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import (IdMixin, TimestampMixin,
                           position_enum_args,
                           milittary_rank_enum_args,
                           academic_rank_enum_args,
                           scientific_degree_enum_args)


class TeacherModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "teachers"

    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    middle_name = Column(String(30), nullable=False)
    position = Column(Enum(*position_enum_args,
                           name="position_enum",
                           schema="load_distribution"), nullable=False)
    military_rank = Column(Enum(*milittary_rank_enum_args,
                                name="military_rank_enum",
                                schema="load_distribution"))
    academic_rank = Column(Enum(*academic_rank_enum_args,
                                name="academic_rank_enum",
                                schema="load_distribution"))
    scientific_degree = Column(Enum(*scientific_degree_enum_args,
                                    name="scientific_degree_enum",
                                    schema="load_distribution"))
    years_of_service = Column(SmallInteger)
    teacher_rate = Column(Numeric(4, 2), nullable=False)
    is_civilian = Column(Boolean, nullable=False)

    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)

    department = relationship("DepartmentModel", back_populates="teachers")
    academic_workloads = relationship(
        argument="AcademicWorkloadTeacherModel",
        back_populates="teacher",
        lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint("last_name", "first_name", "middle_name", name="teachers_full_name_unique_combination"),
        CheckConstraint("1 <= years_of_service <= 50"),
        CheckConstraint("0.25 <= teacher_rate <= 5.00"),
        CheckConstraint(
            "(is_civilian = true AND military_rank IS NULL AND years_of_service IS NULL) "
            "OR (is_civilian = false AND military_rank IS NOT NULL AND years_of_service IS NOT NULL)",
            name="teachers_is_civilian_check"
        )
    )

    def to_read_model(self) -> TeacherSchema:
        return TeacherSchema.from_orm(self)
