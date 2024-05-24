from sqlalchemy import select

from ..models import DepartmentModel
from ..schemas import DepartmentWithTeachersSchema
from ..utils.repository import SQLAlchemyRepository


class DepartmentRepository(SQLAlchemyRepository):
    model = DepartmentModel

    async def get_all_with_teachers(self, **filter_by) -> list[DepartmentWithTeachersSchema]:
        from loguru import logger
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        departments = result.scalars().all()
        return [row.to_read_model_with_teachers() for row in departments]
