from ..exceptions import DisciplineNotFoundException, UserConflictException
from ..schemas import DisciplineWithRelationships, UserSchema
from ..utils.schema import RoleEnum
from ..utils.unit_of_work import IUnitOfWork


class DisciplineService:
    @staticmethod
    async def get_disciplines(uow: IUnitOfWork, user: UserSchema) -> list[DisciplineWithRelationships]:
        async with uow:
            if user.role == RoleEnum.admin:
                return await uow.disciplines.get_all()
            elif user.role == RoleEnum.user:
                if not user.department_id:
                    raise UserConflictException(message="The user has not been assigned a department")
                return await uow.disciplines.get_all(department_id=user.department_id)

    @staticmethod
    async def get_discipline_by_id(uow: IUnitOfWork, discipline_id: str) -> DisciplineWithRelationships:
        async with uow:
            discipline = await uow.disciplines.get_one(id=discipline_id)
            if not discipline:
                raise DisciplineNotFoundException(discipline_id)
            return discipline
