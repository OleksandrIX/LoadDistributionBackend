from ..models import AcademicWorkloadTeacherModel
from ..utils.repository import SQLAlchemyRepository


class AcademicWorkloadTeacherRepository(SQLAlchemyRepository):
    model = AcademicWorkloadTeacherModel
