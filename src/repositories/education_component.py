from ..models import EducationComponentModel
from ..utils.repository import SQLAlchemyRepository


class EducationComponentRepository(SQLAlchemyRepository):
    model = EducationComponentModel
