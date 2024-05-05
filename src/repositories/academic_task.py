from ..models import AcademicTaskModel
from ..utils.repository import SQLAlchemyRepository


class AcademicTaskRepository(SQLAlchemyRepository):
    model = AcademicTaskModel
