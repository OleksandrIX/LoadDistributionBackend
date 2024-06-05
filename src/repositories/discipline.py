from sqlalchemy import select

from ..models import DisciplineModel
from ..utils.repository import SQLAlchemyRepository


class DisciplineRepository(SQLAlchemyRepository):
    model = DisciplineModel

    async def get_all_disciplines_id(self):
        query = select(self.model)
        result = await self.session.execute(query)
        entities = result.scalars().all()
        return [row.to_read_model().id for row in entities]
