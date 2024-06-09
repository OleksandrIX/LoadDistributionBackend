from sqlalchemy import Column, String, TEXT

from ..schemas import WorkloadFormulaSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin


class WorkloadFormulaModel(LoadDistributionBase, IdMixin):
    __tablename__ = "workload_formulas"

    description = Column(TEXT, nullable=False)
    workload_name = Column(String(65), nullable=False)
    formula = Column(TEXT, nullable=False)

    def to_read_model(self) -> WorkloadFormulaSchema:
        return WorkloadFormulaSchema.from_orm(self)
