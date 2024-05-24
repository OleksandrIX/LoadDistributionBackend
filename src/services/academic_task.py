from ..schemas import AcademicTaskSchema, AcademicTaskCreateSchema, AcademicTaskUpdateSchema
from ..exceptions import AcademicTaskNotFoundException, AcademicTaskConflictException
from ..exceptions import ConflictException
from ..utils.unit_of_work import IUnitOfWork


class AcademicTaskService:
    @staticmethod
    async def get_academic_tasks(uow: IUnitOfWork) -> list[AcademicTaskSchema]:
        async with uow:
            return await uow.academic_tasks.get_all()

    @staticmethod
    async def get_academic_task_by_id(uow: IUnitOfWork, academic_task_id: str) -> AcademicTaskSchema:
        async with uow:
            academic_task = await uow.academic_tasks.get_one(id=academic_task_id)
            if not academic_task:
                raise AcademicTaskNotFoundException(academic_task_id)
            return academic_task

    @staticmethod
    async def create_academic_task(uow: IUnitOfWork, academic_task: AcademicTaskCreateSchema) -> str:
        academic_task_dict = academic_task.model_dump()
        async with uow:
            try:
                academic_task: AcademicTaskSchema = await uow.academic_tasks.create_one(data=academic_task_dict)
                await uow.commit()
                return str(academic_task.id)
            except ConflictException:
                raise AcademicTaskConflictException()

    @staticmethod
    async def edit_academic_task(uow: IUnitOfWork,
                                 academic_task_id: str,
                                 academic_task: AcademicTaskUpdateSchema) -> AcademicTaskSchema:
        academic_task_dict = academic_task.model_dump()
        async with uow:
            try:
                is_exists = await uow.academic_tasks.is_exists(id=academic_task_id)
                if not is_exists:
                    raise AcademicTaskNotFoundException(academic_task_id)
                updated_academic_task = await uow.academic_tasks.edit_one(updated_data=academic_task_dict,
                                                                          id=academic_task_id)
                await uow.commit()
                return updated_academic_task
            except ConflictException:
                raise AcademicTaskConflictException()

    @staticmethod
    async def delete_academic_task(uow: IUnitOfWork, academic_task_id: str) -> None:
        async with uow:
            is_exists = await uow.academic_tasks.is_exists(id=academic_task_id)
            if not is_exists:
                raise AcademicTaskNotFoundException(academic_task_id)
            await uow.academic_tasks.delete_one(id=academic_task_id)
            await uow.commit()
