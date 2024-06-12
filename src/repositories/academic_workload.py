from ..models import AcademicWorkloadModel
from ..utils.repository import SQLAlchemyRepository


class AcademicWorkloadRepository(SQLAlchemyRepository):
    model = AcademicWorkloadModel
