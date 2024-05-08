from ..models import EducationComponentsStudyGroupsModel
from ..utils.repository import SQLAlchemyRepository


class EducationComponentsStudyGroupsRepository(SQLAlchemyRepository):
    model = EducationComponentsStudyGroupsModel
