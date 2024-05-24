from ..schemas import SpecialtySchema, SpecialtyCreateSchema, SpecialtyUpdateSchema
from ..exceptions import SpecialtyNotFoundException, SpecialtyConflictException
from ..exceptions import ConflictException
from ..utils.unit_of_work import IUnitOfWork


class SpecialtyService:
    @staticmethod
    async def get_specialties(uow: IUnitOfWork) -> list[SpecialtySchema]:
        async with uow:
            return await uow.specialties.get_all()

    @staticmethod
    async def get_specialty_by_id(uow: IUnitOfWork, specialty_id: str) -> SpecialtySchema:
        async with uow:
            specialty = await uow.specialties.get_one(id=specialty_id)
            if not specialty:
                raise SpecialtyNotFoundException(specialty_id)
            return specialty

    @staticmethod
    async def create_specialty(uow: IUnitOfWork, specialty: SpecialtyCreateSchema) -> str:
        specialty_dict = specialty.model_dump()
        async with uow:
            try:
                specialty: SpecialtySchema = await uow.specialties.create_one(data=specialty_dict)
                await uow.commit()
                return str(specialty.id)
            except ConflictException:
                raise SpecialtyConflictException()

    @staticmethod
    async def edit_specialty(uow: IUnitOfWork, specialty_id: str, specialty: SpecialtyUpdateSchema) -> SpecialtySchema:
        specialty_dict = specialty.model_dump()
        async with uow:
            try:
                is_exists = await uow.specialties.is_exists(id=specialty_id)
                if not is_exists:
                    raise SpecialtyNotFoundException(specialty_id)
                updated_specialty = await uow.specialties.edit_one(updated_data=specialty_dict, id=specialty_id)
                await uow.commit()
                return updated_specialty
            except ConflictException:
                raise SpecialtyConflictException()

    @staticmethod
    async def delete_specialty(uow: IUnitOfWork, specialty_id: str) -> None:
        async with uow:
            is_exists = await uow.specialties.is_exists(id=specialty_id)
            if not is_exists:
                raise SpecialtyNotFoundException(specialty_id)
            await uow.specialties.delete_one(id=specialty_id)
            await uow.commit()
