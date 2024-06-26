from fastapi import APIRouter
from loguru import logger

from ..schemas import StudyGroupSchema, StudyGroupCreateSchema, StudyGroupUpdateSchema
from ..services import StudyGroupService
from ..utils.dependencies import UOWDependencies, SecurityDependencies, AdminDependencies

router = APIRouter(
    prefix="/api/v1/study-groups",
    tags=["Study group"],
    dependencies=[SecurityDependencies]
)


@router.get(
    path="",
    response_model=list[StudyGroupSchema],
    status_code=200,
    dependencies=[AdminDependencies]
)
async def get_study_groups(uow: UOWDependencies) -> list[StudyGroupSchema]:
    return await StudyGroupService.get_study_groups(uow)


@router.get(
    path="/{study_group_id}",
    response_model=StudyGroupSchema,
    status_code=200,
    dependencies=[AdminDependencies]
)
async def get_study_group_by_id(uow: UOWDependencies, study_group_id: str) -> StudyGroupSchema:
    return await StudyGroupService.get_study_group_by_id(uow, study_group_id)


@router.post(
    path="",
    response_model=str,
    status_code=201,
    dependencies=[AdminDependencies]
)
async def create_study_group(uow: UOWDependencies, study_group: StudyGroupCreateSchema) -> str:
    study_group_id = await StudyGroupService.create_study_group(uow, study_group)
    logger.success(f"Created study group with id '{study_group_id}'")
    return study_group_id


@router.put(
    path="/{study_group_id}",
    response_model=StudyGroupSchema,
    status_code=200,
    dependencies=[AdminDependencies]
)
async def edit_study_group(uow: UOWDependencies,
                           study_group_id: str,
                           study_group: StudyGroupUpdateSchema) -> StudyGroupSchema:
    updated_study_group = await StudyGroupService.edit_study_group(uow, study_group_id, study_group)
    logger.success(f"Updated study group with id '{study_group_id}'")
    return updated_study_group


@router.delete(
    path="/{study_group_id}",
    response_model=None,
    status_code=204,
    dependencies=[AdminDependencies]
)
async def delete_study_group(uow: UOWDependencies, study_group_id: str) -> None:
    await StudyGroupService.delete_study_group(uow, study_group_id)
    logger.success(f"Deleted study group with id '{study_group_id}'")
