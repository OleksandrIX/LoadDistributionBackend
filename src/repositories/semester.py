from ..models import SemesterModel
from ..utils.repository import SQLAlchemyRepository


class SemesterRepository(SQLAlchemyRepository):
    model = SemesterModel
