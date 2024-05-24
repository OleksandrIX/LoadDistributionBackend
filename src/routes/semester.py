from fastapi import APIRouter
from loguru import logger

from ..schemas import SemesterSchema, SemesterCreateSchema, SemesterUpdateSchema
from ..services import SemesterService
from ..utils.dependencies import UOWDependencies, SecurityDependencies

router = APIRouter(
    prefix="/api/v1/semesters",
    tags=["Semester"],
    dependencies=[SecurityDependencies]
)


@router.get(
    path="/{semester_id}",
    response_model=SemesterSchema,
    status_code=200
)
async def get_semester_by_id(uow: UOWDependencies, semester_id: str) -> SemesterSchema:
    return await SemesterService.get_semester_by_id(uow, semester_id)


@router.post(
    path="",
    response_model=str,
    status_code=201
)
async def create_semester(uow: UOWDependencies, semester: SemesterCreateSchema) -> str:
    semester_id = await SemesterService.create_semester(uow, semester)
    logger.success(f"Created semester with id '{semester_id}'")
    return semester_id


@router.put(
    path="/{semester_id}",
    response_model=SemesterSchema,
    status_code=200
)
async def edit_semester(uow: UOWDependencies, semester_id: str, semester: SemesterUpdateSchema) -> SemesterSchema:
    updated_semester = await SemesterService.edit_semester(uow, semester_id, semester)
    logger.success(f"Updated semester with id '{semester_id}'")
    return updated_semester


@router.delete(
    path="/{semester_id}",
    response_model=None,
    status_code=204
)
async def delete_semester(uow: UOWDependencies, semester_id: str) -> None:
    await SemesterService.delete_semester(uow, semester_id)
    logger.success(f"Deleted semester with id '{semester_id}'")
