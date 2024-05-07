from loguru import logger
from fastapi import APIRouter

from ..services import SemesterService
from ..schemas import SemesterSchema, SemesterCreateSchema, SemesterUpdateSchema
from ..utils.dependencies import UOWDependencies

router = APIRouter(
    prefix="/api/v1/semesters",
    tags=["Semester"],
)


@router.get("", response_model=list[SemesterSchema], status_code=200)
async def get_semesters(uow: UOWDependencies) -> list[SemesterSchema]:
    return await SemesterService.get_semesters(uow)


@router.get("/{semester_id}", response_model=SemesterSchema, status_code=200)
async def get_semester_by_id(uow: UOWDependencies, semester_id: str) -> SemesterSchema:
    return await SemesterService.get_semester_by_id(uow, semester_id)


@router.post("", response_model=str, status_code=201)
async def create_semester(uow: UOWDependencies, semester: SemesterCreateSchema) -> str:
    semester_id = await SemesterService.create_semester(uow, semester)
    logger.success(f"Created semester with id '{semester_id}'")
    return semester_id


@router.put("/{semester_id}", response_model=SemesterSchema, status_code=200)
async def edit_semester(uow: UOWDependencies, semester_id: str, semester: SemesterUpdateSchema) -> SemesterSchema:
    updated_semester = await SemesterService.edit_semester(uow, semester_id, semester)
    logger.success(f"Updated semester with id '{semester_id}'")
    return updated_semester


@router.delete("/{semester_id}", response_model=None, status_code=204)
async def delete_semester(uow: UOWDependencies, semester_id: str) -> None:
    await SemesterService.delete_semester(uow, semester_id)
    logger.success(f"Deleted semester with id '{semester_id}'")
