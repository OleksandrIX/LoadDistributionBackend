from ..models import AcademicWorkloadFormulaModel
from ..utils.repository import SQLAlchemyRepository


class AcademicWorkloadFormulaRepository(SQLAlchemyRepository):
    model = AcademicWorkloadFormulaModel
