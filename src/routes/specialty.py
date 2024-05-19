from fastapi import APIRouter
from loguru import logger

from ..schemas import SpecialtySchema, SpecialtyCreateSchema, SpecialtyUpdateSchema
from ..services import SpecialtyService
from ..utils.dependencies import UOWDependencies, SecurityDependencies

router = APIRouter(
    prefix="/api/v1/specialties",
    tags=["Specialty"],
    dependencies=[SecurityDependencies]
)


@router.get(
    path="",
    response_model=list[SpecialtySchema],
    status_code=200
)
async def get_specialties(uow: UOWDependencies) -> list[SpecialtySchema]:
    return await SpecialtyService.get_specialties(uow)


@router.get(
    path="/{specialty_id}",
    response_model=SpecialtySchema,
    status_code=200
)
async def get_specialty_by_id(uow: UOWDependencies, specialty_id: str) -> SpecialtySchema:
    return await SpecialtyService.get_specialty_by_id(uow, specialty_id)


@router.post(
    path="",
    response_model=str,
    status_code=201
)
async def create_specialty(uow: UOWDependencies, specialty: SpecialtyCreateSchema) -> str:
    specialty_id = await SpecialtyService.create_specialty(uow, specialty)
    logger.success(f"Created specialty with id '{specialty_id}'")
    return specialty_id


@router.put(
    path="/{specialty_id}",
    response_model=SpecialtySchema,
    status_code=200
)
async def edit_specialty(uow: UOWDependencies, specialty_id: str, specialty: SpecialtyUpdateSchema) -> SpecialtySchema:
    updated_specialty = await SpecialtyService.edit_specialty(uow, specialty_id, specialty)
    logger.success(f"Updated specialty with id '{specialty_id}")
    return updated_specialty


@router.delete(
    path="/{specialty_id}",
    response_model=None,
    status_code=204
)
async def delete_specialty(uow: UOWDependencies, specialty_id: str) -> None:
    await SpecialtyService.delete_specialty(uow, specialty_id)
    logger.success(f"Deleted specialty with id '{specialty_id}'")
