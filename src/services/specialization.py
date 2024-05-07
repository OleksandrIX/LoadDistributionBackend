from ..schemas import SpecializationSchema, SpecializationCreateSchema, SpecializationUpdateSchema
from ..exceptions import SpecializationNotFoundException, SpecializationConflictException
from ..exceptions import ConflictException
from ..utils.unit_of_work import IUnitOfWork


class SpecializationService:
    @staticmethod
    async def get_specializations(uow: IUnitOfWork) -> list[SpecializationSchema]:
        async with uow:
            return await uow.specializations.get_all()

    @staticmethod
    async def get_specialization_by_id(uow: IUnitOfWork, specialization_id: str) -> SpecializationSchema:
        async with uow:
            specialization = await uow.specializations.get_one(id=specialization_id)
            if not specialization:
                raise SpecializationNotFoundException(specialization_id)
            return specialization

    @staticmethod
    async def create_specialization(uow: IUnitOfWork, specialization: SpecializationCreateSchema) -> str:
        specialization_dict = specialization.model_dump()
        async with uow:
            try:
                specialization_id = await uow.specializations.add_one(data=specialization_dict)
                await uow.commit()
                return specialization_id
            except ConflictException:
                raise SpecializationConflictException()

    @staticmethod
    async def edit_specialization(uow: IUnitOfWork,
                                  specialization_id: str,
                                  specialization: SpecializationUpdateSchema) -> SpecializationSchema:
        specialization_dict = specialization.model_dump()
        async with uow:
            try:
                is_exists = await uow.specializations.is_exists(id=specialization_id)
                if not is_exists:
                    raise SpecializationNotFoundException(specialization_id)
                updated_specialization = await uow.specializations.edit_one(updated_data=specialization_dict,
                                                                            id=specialization_id)
                await uow.commit()
                return updated_specialization
            except ConflictException:
                raise SpecializationConflictException()

    @staticmethod
    async def delete_specialization(uow: IUnitOfWork, specialization_id: str) -> None:
        async with uow:
            is_exists = await uow.specializations.is_exists(id=specialization_id)
            if not is_exists:
                raise SpecializationNotFoundException(specialization_id)
            await uow.specializations.delete_one(id=specialization_id)
            await uow.commit()
