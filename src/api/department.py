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


@router.get("/{department_id}", response_model=DepartmentSchema, status_code=200)
async def get_department_by_id(uow: UOWDependencies, department_id: str) -> DepartmentSchema:
    return await DepartmentService.get_department_by_id(uow, department_id)


@router.post("", response_model=str, status_code=201)
async def create_department(uow: UOWDependencies, department: DepartmentCreateSchema) -> str:
    department_id = await DepartmentService.create_department(uow, department)
    logger.success(f"Created department with id '{department_id}'")
    return str(department_id)


@router.put("/{department_id}", response_model=DepartmentSchema, status_code=200)
async def edit_department(uow: UOWDependencies,
                          department_id: str,
                          department: DepartmentUpdateSchema) -> DepartmentSchema:
    updated_department = await DepartmentService.edit_department(uow, department_id, department)
    logger.success(f"Updated department with id '{department_id}")
    return updated_department


@router.delete("/{department_id}", response_model=None, status_code=204)
async def delete_department(uow: UOWDependencies, department_id: str) -> None:
    await DepartmentService.delete_department(uow, department_id)
    logger.success(f"Deleted department with id '{department_id}'")
