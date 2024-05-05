from ..models import AcademicHoursModel
from ..utils.repository import SQLAlchemyRepository


class AcademicHoursRepository(SQLAlchemyRepository):
    model = AcademicHoursModel
