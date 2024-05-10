from loguru import logger
from fastapi import APIRouter
from fastapi_pagination import paginate
from fastapi_pagination.links import Page

from ..services import SpecialtyService
from ..schemas import SpecialtySchema, SpecialtyCreateSchema, SpecialtyUpdateSchema
from ..utils.dependencies import UOWDependencies

router = APIRouter(
    prefix="/routes/v1/specialties",
    tags=["Specialty"],
)


@router.get("", response_model=Page[SpecialtySchema], status_code=200)
async def get_specialties(uow: UOWDependencies) -> Page[SpecialtySchema]:
    return paginate(await SpecialtyService.get_specialties(uow))


@router.get("/{specialty_id}", response_model=SpecialtySchema, status_code=200)
async def get_specialty_by_id(uow: UOWDependencies, specialty_id: str) -> SpecialtySchema:
    return await SpecialtyService.get_specialty_by_id(uow, specialty_id)


@router.post("", response_model=str, status_code=201)
async def create_specialty(uow: UOWDependencies, specialty: SpecialtyCreateSchema) -> str:
    specialty_id = await SpecialtyService.create_specialty(uow, specialty)
    logger.success(f"Created specialty with id '{specialty_id}'")
    return specialty_id


@router.put("/{specialty_id}", response_model=SpecialtySchema, status_code=200)
async def edit_specialty(uow: UOWDependencies, specialty_id: str, specialty: SpecialtyUpdateSchema) -> SpecialtySchema:
    updated_specialty = await SpecialtyService.edit_specialty(uow, specialty_id, specialty)
    logger.success(f"Updated specialty with id '{specialty_id}")
    return updated_specialty


@router.delete("/{specialty_id}", response_model=None, status_code=204)
async def delete_specialty(uow: UOWDependencies, specialty_id: str) -> None:
    await SpecialtyService.delete_specialty(uow, specialty_id)
    logger.success(f"Deleted specialty with id '{specialty_id}'")
