from fastapi import APIRouter
from loguru import logger

from ..schemas import (DepartmentSchema,
                       DepartmentCreateSchema,
                       DepartmentUpdateSchema,
                       DepartmentWithTeachersSchema,
                       DepartmentWithEducationComponentsSchema)
from ..services import DepartmentService
from ..utils.dependencies import UOWDependencies, SecurityDependencies, AdminDependencies, AccessControlDependencies

router = APIRouter(
    prefix="/api/v1/departments",
    tags=["Department"],
    dependencies=[SecurityDependencies]
)


@router.get(
    path="",
    response_model=list[DepartmentSchema],
    status_code=200,
    dependencies=[AdminDependencies]
)
async def get_departments(uow: UOWDependencies) -> list[DepartmentSchema]:
    return await DepartmentService.get_departments(uow)


@router.get(
    path="/teachers",
    response_model=list[DepartmentWithTeachersSchema],
    status_code=200,
    dependencies=[AdminDependencies]
)
async def get_departments(uow: UOWDependencies) -> list[DepartmentWithTeachersSchema]:
    return await DepartmentService.get_department_with_teachers(uow)


@router.get(
    path="/education-components",
    response_model=list[DepartmentWithEducationComponentsSchema],
    status_code=200,
    dependencies=[AdminDependencies]
)
async def get_department_by_id(uow: UOWDependencies) -> list[DepartmentWithEducationComponentsSchema]:
    return await DepartmentService.get_department_with_education_components(uow)


@router.get(
    path="/{department_id}",
    response_model=DepartmentSchema,
    status_code=200,
    dependencies=[AccessControlDependencies]
)
async def get_department_by_id(uow: UOWDependencies, department_id: str) -> DepartmentSchema:
    return await DepartmentService.get_department_by_id(uow, department_id)


@router.get(
    path="/{department_id}/teachers",
    response_model=DepartmentWithTeachersSchema,
    status_code=200,
    dependencies=[AccessControlDependencies]
)
async def get_department_by_id(uow: UOWDependencies, department_id: str) -> DepartmentWithTeachersSchema:
    return await DepartmentService.get_deparment_by_id_with_teachers(uow, department_id)


@router.get(
    path="/{department_id}/education-components",
    response_model=DepartmentWithEducationComponentsSchema,
    status_code=200,
    dependencies=[AccessControlDependencies]
)
async def get_department_by_id(uow: UOWDependencies, department_id: str) -> DepartmentWithEducationComponentsSchema:
    return await DepartmentService.get_deparment_by_id_with_education_components(uow, department_id)


@router.post(
    path="",
    response_model=str,
    status_code=201,
    dependencies=[AdminDependencies]
)
async def create_department(uow: UOWDependencies, department: DepartmentCreateSchema) -> str:
    department_id = await DepartmentService.create_department(uow, department)
    logger.success(f"Created department with id '{department_id}'")
    return department_id


@router.put(
    path="/{department_id}",
    response_model=DepartmentSchema,
    status_code=200,
    dependencies=[AdminDependencies]
)
async def edit_department(uow: UOWDependencies,
                          department_id: str,
                          department: DepartmentUpdateSchema) -> DepartmentSchema:
    updated_department = await DepartmentService.edit_department(uow, department_id, department)
    logger.success(f"Updated department with id '{department_id}")
    return updated_department


@router.delete(
    path="/{department_id}",
    response_model=None,
    status_code=204,
    dependencies=[AdminDependencies]
)
async def delete_department(uow: UOWDependencies, department_id: str) -> None:
    await DepartmentService.delete_department(uow, department_id)
    logger.success(f"Deleted department with id '{department_id}'")
