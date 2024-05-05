from ..models import StudyGroupModel
from ..utils.repository import SQLAlchemyRepository


class StudyGroupRepository(SQLAlchemyRepository):
    model = StudyGroupModel
