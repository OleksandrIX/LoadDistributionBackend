from ..models import SpecializationModel
from ..utils.repository import SQLAlchemyRepository


class SpecializationRepository(SQLAlchemyRepository):
    model = SpecializationModel
