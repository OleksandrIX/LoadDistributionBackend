from ..schemas import DisciplineSchema, DisciplineWithRelationships

from ..exceptions import DisciplineNotFoundException

from ..utils.unit_of_work import IUnitOfWork


class DisciplineService:
    @staticmethod
    async def get_disciplines(uow: IUnitOfWork) -> list[DisciplineSchema]:
        async with uow:
            return await uow.disciplines.get_all()

    @staticmethod
    async def get_discipline_by_id(uow: IUnitOfWork, discipline_id: str) -> DisciplineSchema:
        async with uow:
            discipline = await uow.disciplines.get_one(id=discipline_id)
            if not discipline:
                raise DisciplineNotFoundException(discipline_id)
            return discipline
