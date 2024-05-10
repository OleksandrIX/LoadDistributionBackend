from loguru import logger
from fastapi import APIRouter
from fastapi_pagination import paginate
from fastapi_pagination.links import Page

from ..services import AcademicTaskService
from ..schemas import AcademicTaskSchema, AcademicTaskCreateSchema, AcademicTaskUpdateSchema
from ..utils.dependencies import UOWDependencies

router = APIRouter(
    prefix="/api/v1/academic-tasks",
    tags=["Academic task"]
)


@router.get("", response_model=Page[AcademicTaskSchema], status_code=200)
async def get_academic_tasks(uow: UOWDependencies) -> Page[AcademicTaskSchema]:
    return paginate(await AcademicTaskService.get_academic_tasks(uow))


@router.get("/{academic_task_id}", response_model=AcademicTaskSchema, status_code=200)
async def get_academic_task_by_id(uow: UOWDependencies, academic_task_id: str) -> AcademicTaskSchema:
    return await AcademicTaskService.get_academic_task_by_id(uow, academic_task_id)


@router.post("", response_model=str, status_code=200)
async def create_academic_task(uow: UOWDependencies, academic_task: AcademicTaskCreateSchema) -> str:
    academic_task_id = await AcademicTaskService.create_academic_task(uow, academic_task)
    logger.success(f"Created academic task with id '{academic_task_id}'")
    return academic_task_id


@router.put("/{academic_task_id}", response_model=AcademicTaskSchema, status_code=200)
async def edit_academic_task(uow: UOWDependencies,
                             academic_task_id: str,
                             academic_task: AcademicTaskUpdateSchema) -> AcademicTaskSchema:
    updated_academic_task = await AcademicTaskService.edit_academic_task(uow, academic_task_id, academic_task)
    logger.success(f"Updated academic task with id '{academic_task_id}'")
    return updated_academic_task


@router.delete("/{academic_task_id}", response_model=None, status_code=200)
async def delete_academic_task(uow: UOWDependencies, academic_task_id: str) -> None:
    await AcademicTaskService.delete_academic_task(uow, academic_task_id)
    logger.success(f"Deleted academic task with id '{academic_task_id}'")
