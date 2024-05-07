from loguru import logger
from fastapi import APIRouter

from ..services import DepartmentService
from ..schemas import DepartmentSchema, DepartmentCreateSchema, DepartmentUpdateSchema
from ..utils.dependencies import UOWDependencies

router = APIRouter(
    prefix="/api/v1/departments",
    tags=["Department"]
)


@router.get("", response_model=list[DepartmentSchema], status_code=200)
async def get_departments(uow: UOWDependencies) -> list[DepartmentSchema]:
    return await DepartmentService.get_departments(uow)


@router.get("/{id}", response_model=DepartmentSchema, status_code=200)
async def get_department_by_id(uow: UOWDependencies, id: str) -> DepartmentSchema:
    return await DepartmentService.get_department_by_id(uow, id)


@router.post("", response_model=str, status_code=201)
async def get_departments(uow: UOWDependencies, departmnet: DepartmentCreateSchema) -> str:
    departmnet_id = await DepartmentService.create_department(uow, departmnet)
    logger.success(f"Created department with id '{departmnet_id}'")
    return str(departmnet_id)


@router.put("/{id}", response_model=DepartmentSchema, status_code=200)
async def edit_department(uow: UOWDependencies, id: str, department: DepartmentUpdateSchema) -> DepartmentSchema:
    updated_department = await DepartmentService.edit_department(uow, id, department)
    logger.success(f"Updated department with id '{id}")
    return updated_department


@router.delete("/{id}", status_code=204)
async def get_departments(uow: UOWDependencies, id: str) -> None:
    await DepartmentService.delete_department(uow, id)
    logger.success(f"Deleted department with id '{id}'")
