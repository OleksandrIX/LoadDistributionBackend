from sqlalchemy import Column, String, TEXT

from ..schemas import AcademicWorkloadFormulaSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin


class AcademicWorkloadFormulaModel(LoadDistributionBase, IdMixin):
    __tablename__ = "academic_workload_formulas"

    description = Column(TEXT, nullable=False)
    workload_name = Column(String(65), nullable=False)
    formula = Column(TEXT, nullable=False)

    def to_read_model(self) -> AcademicWorkloadFormulaSchema:
        return AcademicWorkloadFormulaSchema.from_orm(self)
