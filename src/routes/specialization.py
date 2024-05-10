from loguru import logger
from fastapi import APIRouter
from fastapi_pagination import paginate
from fastapi_pagination.links import Page

from ..services import SpecializationService
from ..schemas import SpecializationSchema, SpecializationCreateSchema, SpecializationUpdateSchema
from ..utils.dependencies import UOWDependencies

router = APIRouter(
    prefix="/routes/v1/specializations",
    tags=["Specialization"],
)


@router.get("", response_model=Page[SpecializationSchema], status_code=200)
async def get_specializations(uow: UOWDependencies) -> Page[SpecializationSchema]:
    return paginate(await SpecializationService.get_specializations(uow))


@router.get("/{specialization_id}", response_model=SpecializationSchema, status_code=200)
async def get_specialization_by_id(uow: UOWDependencies, specialization_id: str) -> SpecializationSchema:
    return await SpecializationService.get_specialization_by_id(uow, specialization_id)


@router.post("", response_model=str, status_code=201)
async def create_specialization(uow: UOWDependencies,
                                specialization: SpecializationCreateSchema) -> str:
    specialization_id = await SpecializationService.create_specialization(uow, specialization)
    logger.success(f"Created specialization with id '{specialization_id}'")
    return specialization_id


@router.put("/{specialization_id}", response_model=SpecializationSchema, status_code=200)
async def edit_specialization(uow: UOWDependencies,
                              specialization_id: str,
                              specialization: SpecializationUpdateSchema) -> SpecializationSchema:
    updated_specialization = await SpecializationService.edit_specialization(uow, specialization_id, specialization)
    logger.success(f"Updated specialization with id '{specialization_id}")
    return updated_specialization


@router.delete("/{specialization_id}", response_model=None, status_code=204)
async def delete_specialization(uow: UOWDependencies, specialization_id: str) -> None:
    await SpecializationService.delete_specialization(uow, specialization_id)
    logger.success(f"Deleted specialization with id '{specialization_id}'")
