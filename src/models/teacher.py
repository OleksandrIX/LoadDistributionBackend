from sqlalchemy import Column, Enum, String, SmallInteger, CheckConstraint, UUID, ForeignKey, UniqueConstraint
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
                                schema="load_distribution"), nullable=False)
    academic_rank = Column(Enum(*academic_rank_enum_args,
                                name="academic_rank_enum",
                                schema="load_distribution"), nullable=False)
    scientific_degree = Column(Enum(*scientific_degree_enum_args,
                                    name="scientific_degree_enum",
                                    schema="load_distribution"), nullable=False)
    years_of_service = Column(SmallInteger, nullable=False)

    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)

    department = relationship("DepartmentModel", back_populates="teachers")

    __table_args__ = (
        UniqueConstraint("last_name", "first_name", "middle_name", name="teachers_full_name_unique_combination"),
        CheckConstraint("1 <= years_of_service <= 50")
    )

    def to_read_model(self) -> TeacherSchema:
        return TeacherSchema(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            position=self.position,
            military_rank=self.military_rank,
            academic_rank=self.academic_rank,
            scientific_degree=self.scientific_degree,
            years_of_service=self.years_of_service,
            department_id=str(self.department_id),
            created_at=self.created_at,
            updated_at=self.updated_at
        )
