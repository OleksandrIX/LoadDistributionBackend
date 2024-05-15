from ..models import TeacherModel
from ..utils.repository import SQLAlchemyRepository


class TeacherRepository(SQLAlchemyRepository):
    model = TeacherModel
