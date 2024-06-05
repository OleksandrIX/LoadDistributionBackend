from ..models import WorkloadFormulaModel
from ..utils.repository import SQLAlchemyRepository


class AcademicWorkloadFormulaRepository(SQLAlchemyRepository):
    model = WorkloadFormulaModel
