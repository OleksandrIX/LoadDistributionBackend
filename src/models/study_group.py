from sqlalchemy import Column, Enum, String, SmallInteger, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship

from ..utils.database import Base
from .core import IdMixin, TimestampMixin

from .many_to_many_tables import education_components_study_groups


class StudyGroupModel(Base, IdMixin, TimestampMixin):
    __tablename__ = "study_groups"

    group_code = Column(String(10), nullable=False)
    course_study = Column(SmallInteger, nullable=False)
    education_degree = Column(Enum("bachelor", "master"), nullable=False)
    number_listeners = Column(SmallInteger, nullable=False)

    education_components = relationship("EducationComponentModel",
                                        education_components_study_groups,
                                        back_populates="study_groups")

    __table_args__ = (
        UniqueConstraint("group_code", "course_study", name="group_unique_constraint"),
        CheckConstraint("1 <= course_study <= 6"),
        CheckConstraint("1 <= number_listeners <= 50")
    )
