from ..models import SpecialtyModel
from ..utils.repository import SQLAlchemyRepository


class SpecialtyRepository(SQLAlchemyRepository):
    model = SpecialtyModel
