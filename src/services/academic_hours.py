from ..schemas import AcademicHoursSchema, AcademicHoursCreateSchema, AcademicHoursUpdateSchema
from ..exceptions import AcademicHoursNotFoundException, AcademicHoursConflictException
from ..exceptions import ConflictException
from ..utils.unit_of_work import IUnitOfWork


class AcademicHoursService:
    @staticmethod
    async def get_academic_hours(uow: IUnitOfWork) -> list[AcademicHoursSchema]:
        async with uow:
            return await uow.academic_hours.get_all()

    @staticmethod
    async def get_academic_hours_by_id(uow: IUnitOfWork, academic_hours_id: str) -> AcademicHoursSchema:
        async with uow:
            academic_hours = await uow.academic_hours.get_one(id=academic_hours_id)
            if not academic_hours:
                raise AcademicHoursNotFoundException(academic_hours_id)
            return academic_hours

    @staticmethod
    async def create_academic_hours(uow: IUnitOfWork, academic_hours: AcademicHoursCreateSchema) -> str:
        academic_hours_dict = academic_hours.model_dump()
        async with uow:
            try:
                academic_hours_id = await uow.academic_hours.add_one(data=academic_hours_dict)
                await uow.commit()
                return str(academic_hours_id)
            except ConflictException:
                raise AcademicHoursConflictException()

    @staticmethod
    async def edit_academic_hours(uow: IUnitOfWork,
                                  academic_hours_id: str,
                                  academic_hours: AcademicHoursUpdateSchema) -> AcademicHoursSchema:
        academic_hours_dict = academic_hours.model_dump()
        async with uow:
            try:
                is_exists = await uow.academic_hours.is_exists(id=academic_hours_id)
                if not is_exists:
                    raise AcademicHoursNotFoundException(academic_hours_id)
                updated_academic_hours = await uow.academic_hours.edit_one(updated_data=academic_hours_dict,
                                                                           id=academic_hours_id)
                await uow.commit()
                return updated_academic_hours
            except ConflictException:
                raise AcademicHoursConflictException()

    @staticmethod
    async def delete_academic_hours(uow: IUnitOfWork, academic_hours_id: str) -> None:
        async with uow:
            is_exists = await uow.academic_hours.is_exists(id=academic_hours_id)
            if not is_exists:
                raise AcademicHoursNotFoundException(academic_hours_id)
            await uow.academic_hours.delete_one(id=academic_hours_id)
            await uow.commit()
