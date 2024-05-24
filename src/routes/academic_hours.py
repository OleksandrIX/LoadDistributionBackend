from fastapi import APIRouter
from loguru import logger

from ..schemas import AcademicHoursSchema, AcademicHoursCreateSchema, AcademicHoursUpdateSchema
from ..services import AcademicHoursService
from ..utils.dependencies import UOWDependencies, SecurityDependencies

router = APIRouter(
    prefix="/api/v1/academic-hours",
    tags=["Academic hours"],
    dependencies=[SecurityDependencies]
)


@router.get(
    path="/{academic_hours_id}",
    response_model=AcademicHoursSchema,
    status_code=200
)
async def get_academic_hours_by_id(uow: UOWDependencies, academic_hours_id: str) -> AcademicHoursSchema:
    return await AcademicHoursService.get_academic_hours_by_id(uow, academic_hours_id)


@router.post(
    path="",
    response_model=str,
    status_code=201
)
async def create_academic_hours(uow: UOWDependencies, academic_hours: AcademicHoursCreateSchema) -> str:
    academic_hours_id = await AcademicHoursService.create_academic_hours(uow, academic_hours)
    logger.success(f"Created academic hours with id '{academic_hours_id}'")
    return academic_hours_id


@router.put(
    path="/{academic_hours_id}",
    response_model=AcademicHoursSchema,
    status_code=200
)
async def edit_academic_hours(uow: UOWDependencies,
                              academic_hours_id: str,
                              academic_hours: AcademicHoursUpdateSchema) -> AcademicHoursSchema:
    updated_academic_hours = await AcademicHoursService.edit_academic_hours(uow, academic_hours_id, academic_hours)
    logger.success(f"Updated academic hours with id '{academic_hours_id}'")
    return updated_academic_hours


@router.delete(
    path="/{academic_hours_id}",
    response_model=None,
    status_code=204
)
async def delete_academic_hours(uow: UOWDependencies, academic_hours_id: str) -> None:
    await AcademicHoursService.delete_academic_hours(uow, academic_hours_id)
    logger.success(f"Deleted academic hours with id '{academic_hours_id}'")
