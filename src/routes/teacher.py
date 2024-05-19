from fastapi import APIRouter
from fastapi_pagination import paginate
from fastapi_pagination.links import Page
from loguru import logger

from ..schemas import TeacherSchema, TeacherCreateSchema, TeacherUpdateSchema
from ..services import TeacherService
from ..utils.dependencies import UOWDependencies, SecurityDependencies, AdminDependencies

router = APIRouter(
    prefix="/api/v1/teachers",
    tags=["Teachers"],
    dependencies=[SecurityDependencies],
)


@router.get("", response_model=Page[TeacherSchema], status_code=200, dependencies=[AdminDependencies])
async def get_teachers(uow: UOWDependencies) -> Page[TeacherSchema]:
    return paginate(await TeacherService.get_teachers(uow))


@router.get("/{teacher_id}", response_model=TeacherSchema, status_code=200)
async def get_teacher_by_id(uow: UOWDependencies, teacher_id: str) -> TeacherSchema:
    return await TeacherService.get_teacher_by_id(uow, teacher_id)


@router.post("", response_model=str, status_code=201)
async def create_teacher(uow: UOWDependencies, teacher: TeacherCreateSchema) -> str:
    teacher_id = await TeacherService.create_teacher(uow, teacher)
    logger.success(f"Created teacher with id '{teacher_id}'")
    return teacher_id


@router.put("/{teacher_id}", response_model=TeacherSchema, status_code=200)
async def edit_teacher(uow: UOWDependencies, teacher_id: str, teacher: TeacherUpdateSchema) -> TeacherSchema:
    updated_teacher = await TeacherService.edit_teacher(uow, teacher_id, teacher)
    logger.success(f"Updated teacher with id '{teacher_id}'")
    return updated_teacher


@router.delete("/{teacher_id}", response_model=None, status_code=204)
async def delete_teacher(uow: UOWDependencies, teacher_id: str) -> None:
    await TeacherService.delete_teacher(uow, teacher_id)
    logger.success(f"Deleted teacher with id '{teacher_id}'")
