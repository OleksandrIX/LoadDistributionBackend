from ..schemas import StudyGroupSchema, StudyGroupCreateSchema, StudyGroupUpdateSchema
from ..exceptions import StudyGroupNotFoundException, StudyGroupConflictException
from ..exceptions import ConflictException
from ..utils.unit_of_work import IUnitOfWork


class StudyGroupService:
    @staticmethod
    async def get_study_groups(uow: IUnitOfWork) -> list[StudyGroupSchema]:
        async with uow:
            return await uow.study_groups.get_all()

    @staticmethod
    async def get_study_group_by_id(uow: IUnitOfWork, study_group_id: str) -> StudyGroupSchema:
        async with uow:
            study_group = await uow.study_groups.get_one(id=study_group_id)
            if not study_group:
                raise StudyGroupNotFoundException(study_group_id)
            return study_group

    @staticmethod
    async def create_study_group(uow: IUnitOfWork, study_group: StudyGroupCreateSchema) -> str:
        study_group_dict = study_group.model_dump()
        async with uow:
            try:
                study_group: StudyGroupSchema = await uow.study_groups.create_one(data=study_group_dict)
                await uow.commit()
                return str(study_group.id)
            except ConflictException:
                raise StudyGroupConflictException()

    @staticmethod
    async def edit_study_group(uow: IUnitOfWork,
                               study_group_id: str,
                               study_group: StudyGroupUpdateSchema) -> StudyGroupSchema:
        study_group_dict = study_group.model_dump()
        async with uow:
            try:
                is_exists = await uow.study_groups.is_exists(id=study_group_id)
                if not is_exists:
                    raise StudyGroupNotFoundException(study_group_id)
                updated_study_group = await uow.study_groups.edit_one(updated_data=study_group_dict, id=study_group_id)
                await uow.commit()
                return updated_study_group
            except ConflictException:
                raise StudyGroupConflictException()

    @staticmethod
    async def delete_study_group(uow: IUnitOfWork, study_group_id: str) -> None:
        async with uow:
            is_exists = await uow.study_groups.is_exists(id=study_group_id)
            if not is_exists:
                raise StudyGroupNotFoundException(study_group_id)
            await uow.study_groups.delete_one(id=study_group_id)
            await uow.commit()
