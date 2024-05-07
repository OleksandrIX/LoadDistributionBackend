from sqlalchemy import Column, Enum, String, SmallInteger, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship

from .many_to_many_tables import education_components_study_groups
from ..schemas import StudyGroupSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class StudyGroupModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "study_groups"

    group_code = Column(String(10), nullable=False)
    course_study = Column(SmallInteger, nullable=False)
    education_degree = Column(Enum("bachelor", "master",
                                   name="education_degree_enum",
                                   schema="load_distribution"), nullable=False)
    number_listeners = Column(SmallInteger, nullable=False)

    education_components = relationship("EducationComponentModel",
                                        education_components_study_groups,
                                        back_populates="study_groups",
                                        lazy="selectin")

    __table_args__ = (
        UniqueConstraint("group_code", "course_study", name="group_unique_constraint"),
        CheckConstraint("1 <= course_study <= 6"),
        CheckConstraint("1 <= number_listeners <= 50")
    )

    def to_read_model(self) -> StudyGroupSchema:
        return StudyGroupSchema(
            id=self.id,
            group_code=self.group_code,
            course_study=self.course_study,
            education_degree=self.education_degree,
            number_listeners=self.number_listeners,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
