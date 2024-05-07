from loguru import logger
from fastapi import APIRouter

from ..services import AcademicHoursService
from ..schemas import AcademicHoursSchema, AcademicHoursCreateSchema, AcademicHoursUpdateSchema
from ..utils.dependencies import UOWDependencies

router = APIRouter(
    prefix="/api/v1/academic-hours",
    tags=["Academic hours"],
)


@router.get("", response_model=list[AcademicHoursSchema], status_code=200)
async def get_academic_hours(uow: UOWDependencies) -> list[AcademicHoursSchema]:
    return await AcademicHoursService.get_academic_hours(uow)


@router.get("/{academic_hours_id}", response_model=AcademicHoursSchema, status_code=200)
async def get_academic_hours_by_id(uow: UOWDependencies, academic_hours_id: str) -> AcademicHoursSchema:
    return await AcademicHoursService.get_academic_hours_by_id(uow, academic_hours_id)


@router.post("", response_model=str, status_code=201)
async def create_academic_hours(uow: UOWDependencies, academic_hours: AcademicHoursCreateSchema) -> str:
    academic_hours_id = await AcademicHoursService.create_academic_hours(uow, academic_hours)
    logger.success(f"Created academic hours with id '{academic_hours_id}'")
    return academic_hours_id


@router.put("/{academic_hours_id}", response_model=AcademicHoursSchema, status_code=200)
async def edit_academic_hours(uow: UOWDependencies,
                              academic_hours_id: str,
                              academic_hours: AcademicHoursUpdateSchema) -> AcademicHoursSchema:
    updated_academic_hours = await AcademicHoursService.edit_academic_hours(uow, academic_hours_id, academic_hours)
    logger.success(f"Updated academic hours with id '{academic_hours_id}'")
    return updated_academic_hours


@router.delete("/{academic_hours_id}", response_model=None, status_code=204)
async def delete_academic_hours(uow: UOWDependencies, academic_hours_id: str) -> None:
    await AcademicHoursService.delete_academic_hours(uow, academic_hours_id)
    logger.success(f"Deleted academic hours with id '{academic_hours_id}'")
