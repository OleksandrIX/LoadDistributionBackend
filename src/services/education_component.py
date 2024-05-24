from ..schemas import EducationComponentSchema, EducationComponentCreateSchema, EducationComponentUpdateSchema
from ..exceptions import EducationComponentNotFoundException, EducationComponentConflictException
from ..exceptions import ConflictException
from ..utils.unit_of_work import IUnitOfWork


class EducationComponentService:
    @staticmethod
    async def get_education_components(uow: IUnitOfWork) -> list[EducationComponentSchema]:
        async with uow:
            return await uow.education_components.get_all()

    @staticmethod
    async def get_education_component_by_id(uow: IUnitOfWork, education_component_id: str) -> EducationComponentSchema:
        async with uow:
            education_component = await uow.education_components.get_one(id=education_component_id)
            if not education_component:
                raise EducationComponentNotFoundException(education_component_id)
            return education_component

    @staticmethod
    async def create_education_component(uow: IUnitOfWork, education_component: EducationComponentCreateSchema) -> str:
        education_component_dict = education_component.model_dump()
        async with uow:
            try:
                education_component: EducationComponentSchema = await uow.education_components.create_one(
                    data=education_component_dict
                )
                await uow.commit()
                return str(education_component.id)
            except ConflictException:
                raise EducationComponentConflictException()

    @staticmethod
    async def edit_education_component(uow: IUnitOfWork,
                                       education_component_id: str,
                                       education_component: EducationComponentUpdateSchema) -> EducationComponentSchema:
        education_component_dict = education_component.model_dump()
        async with uow:
            try:
                is_exists = await uow.education_components.is_exists(id=education_component_id)
                if not is_exists:
                    raise EducationComponentNotFoundException(education_component_id)
                updated_education_component = await uow.education_components.edit_one(
                    updated_data=education_component_dict,
                    id=education_component_id
                )
                await uow.commit()
                return updated_education_component
            except ConflictException:
                raise EducationComponentConflictException()

    @staticmethod
    async def delete_education_component(uow: IUnitOfWork, education_component_id: str) -> None:
        async with uow:
            is_exists = await uow.education_components.is_exists(id=education_component_id)
            if not is_exists:
                raise EducationComponentNotFoundException(education_component_id)
            await uow.education_components.delete_one(id=education_component_id)
            await uow.commit()
