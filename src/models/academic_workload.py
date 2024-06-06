from sqlalchemy import Column, SmallInteger, Numeric, UUID, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from ..schemas import AcademicWorkloadSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class AcademicWorkloadModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "academic_workloads"

    lecture_hours = Column(SmallInteger, nullable=False)
    group_hours = Column(SmallInteger, nullable=False)
    practical_hours = Column(SmallInteger, nullable=False)
    laboratory_reports_checking_hours = Column(Numeric(8, 4), nullable=False)
    special_exercises_conducting_hours = Column(Numeric(8, 4), nullable=False)
    consultation_hours = Column(Numeric(8, 4), nullable=False)
    term_papers_conducting_hours = Column(Numeric(8, 4), nullable=False)
    control_works_checking_hours = Column(Numeric(8, 4), nullable=False)
    graded_tests_conducting_hours = Column(Numeric(8, 4), nullable=False)
    exams_conducting_hours = Column(Numeric(8, 4), nullable=False)
    military_internship_conducting_hours = Column(Numeric(8, 4), nullable=False)
    supervision_qualification_works_hours = Column(Numeric(8, 4), nullable=False)
    qualification_works_defense_conducting_hours = Column(Numeric(8, 4), nullable=False)
    complex_exams_conducting_hours = Column(Numeric(8, 4), nullable=False)
    other_types_conducting_hours = Column(Numeric(8, 4), nullable=False)

    discipline = relationship(
        argument="DisciplineModel",
        back_populates="academic_workload",
        lazy="selectin",
        uselist=False,
    )

    academic_workload_teacher = relationship(
        argument="AcademicWorkloadTeacherModel",
        back_populates="academic_workload",
        lazy="selectin"
    )

    __table_args__ = (
        CheckConstraint(
            sqltext="lecture_hours >= 0 AND lecture_hours <= 10000",
            name="academic_workloads_lecture_hours_check"
        ),
        CheckConstraint(
            sqltext="group_hours >= 0 AND group_hours <= 10000",
            name="academic_workloads_group_hours_check"
        ),
        CheckConstraint(
            sqltext="practical_hours >= 0 AND practical_hours <= 10000",
            name="academic_workloads_practical_hours_check"
        ),
        CheckConstraint(
            sqltext="laboratory_reports_checking_hours >= 0.0 AND laboratory_reports_checking_hours <= 10000.0",
            name="academic_workloads_laboratory_reports_checking_hours_check"
        ),
        CheckConstraint(
            sqltext="special_exercises_conducting_hours >= 0.0 AND special_exercises_conducting_hours <= 10000.0",
            name="academic_workloads_special_exercises_conducting_hours_check"
        ),
        CheckConstraint(
            sqltext="consultation_hours >= 0.0 AND consultation_hours <= 10000.0",
            name="academic_workloads_consultation_hours_check"
        ),
        CheckConstraint(
            sqltext="term_papers_conducting_hours >= 0.0 AND term_papers_conducting_hours <= 10000.0",
            name="academic_workloads_term_papers_conducting_hours_check"
        ),
        CheckConstraint(
            sqltext="control_works_checking_hours >= 0.0 AND control_works_checking_hours <= 10000.0",
            name="academic_workloads_control_works_checking_hours_check"
        ),
        CheckConstraint(
            sqltext="graded_tests_conducting_hours >= 0.0 AND graded_tests_conducting_hours <= 10000.0",
            name="academic_workloads_graded_tests_conducting_hours_check"
        ),
        CheckConstraint(
            sqltext="exams_conducting_hours >= 0.0 AND exams_conducting_hours <= 10000.0",
            name="academic_workloads_exams_conducting_hours_check"
        ),
        CheckConstraint(
            sqltext="military_internship_conducting_hours >= 0.0 AND military_internship_conducting_hours <= 10000.0",
            name="academic_workloads_military_internship_conducting_hours_check"
        ),
        CheckConstraint(
            sqltext="supervision_qualification_works_hours >= 0.0 AND supervision_qualification_works_hours <= 10000.0",
            name="academic_workloads_supervision_qualification_works_hours_check"
        ),
        CheckConstraint(
            sqltext="qualification_works_defense_conducting_hours >= 0.0 "
                    "AND qualification_works_defense_conducting_hours <= 10000.0",
            name="academic_workloads_qw_defense_conducting_hours_check"
        ),
        CheckConstraint(
            sqltext="complex_exams_conducting_hours >= 0.0 AND complex_exams_conducting_hours <= 10000.0",
            name="academic_workloads_complex_exams_conducting_hours_check"
        ),
        CheckConstraint(
            sqltext="other_types_conducting_hours >= 0.0 AND other_types_conducting_hours <= 10000.0",
            name="academic_workloads_other_types_conducting_hours_check"
        )
    )

    def to_read_model(self) -> AcademicWorkloadSchema:
        return AcademicWorkloadSchema.from_orm(self)
