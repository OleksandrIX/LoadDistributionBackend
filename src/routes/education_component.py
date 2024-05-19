from loguru import logger
from fastapi import APIRouter
from fastapi_pagination import paginate
from fastapi_pagination.links import Page

from ..services import EducationComponentService
from ..schemas import EducationComponentSchema, EducationComponentCreateSchema, EducationComponentUpdateSchema
from ..utils.dependencies import UOWDependencies, SecurityDependencies

router = APIRouter(
    prefix="/api/v1/education-components",
    tags=["Education Component"],
    dependencies=[SecurityDependencies]
)


@router.get(
    "",
    response_model=Page[EducationComponentSchema],
    status_code=200
)
async def get_education_components(uow: UOWDependencies) -> Page[EducationComponentSchema]:
    return paginate(await EducationComponentService.get_education_components(uow))


@router.get(
    path="/{education_component_id}",
    response_model=EducationComponentSchema,
    status_code=200
)
async def get_education_component_by_id(uow: UOWDependencies, education_component_id: str) -> EducationComponentSchema:
    return await EducationComponentService.get_education_component_by_id(uow, education_component_id)


@router.post(
    path="",
    response_model=str,
    status_code=201
)
async def create_education_component(uow: UOWDependencies, education_component: EducationComponentCreateSchema) -> str:
    education_component_id = await EducationComponentService.create_education_component(uow, education_component)
    logger.success(f"Created education component with id '{education_component_id}'")
    return education_component_id


@router.put(
    path="/{education_component_id}",
    response_model=EducationComponentSchema,
    status_code=200
)
async def edit_education_component(
        uow: UOWDependencies,
        education_component_id: str,
        education_component: EducationComponentUpdateSchema
) -> EducationComponentSchema:
    updated_education_component = await EducationComponentService.edit_education_component(
        uow,
        education_component_id,
        education_component
    )
    logger.success(f"Updated education component with id '{education_component_id}'")
    return updated_education_component


@router.delete(
    path="/{education_component_id}",
    response_model=None,
    status_code=204
)
async def delete_education_component(uow: UOWDependencies, education_component_id: str) -> None:
    await EducationComponentService.delete_education_component(uow, education_component_id)
    logger.success(f"Deleted education component with id '{education_component_id}'")
