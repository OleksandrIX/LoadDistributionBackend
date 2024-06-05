from ..models import DisciplineModel
from ..utils.repository import SQLAlchemyRepository


class DisciplineRepository(SQLAlchemyRepository):
    model = DisciplineModel
