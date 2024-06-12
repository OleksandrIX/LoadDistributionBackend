from fastapi import APIRouter
from loguru import logger

from ..schemas import AcademicWorkloadSchema, AcademicWorkloadCreateSchema, AcademicWorkloadTeacherSchema
from ..services import AcademicWorkloadService, CalculationAcademicWorkloadService
from ..utils.dependencies import UOWDependencies, SecurityDependencies

router = APIRouter(
    prefix="/api/v1/academic-workloads",
    tags=["Academic Workload"],
    dependencies=[SecurityDependencies]
)


@router.post(
    path="/{discipline_id}/teachers/{teacher_id}",
    response_model=AcademicWorkloadTeacherSchema,
    status_code=201
)
async def create_academic_workload(
        uow: UOWDependencies,
        discipline_id: str,
        teacher_id: str,
        semester_number: int,
        academic_workload: AcademicWorkloadCreateSchema
) -> AcademicWorkloadTeacherSchema:
    saved_academic_workload = await CalculationAcademicWorkloadService.save_academic_workload(uow, academic_workload)
    return await AcademicWorkloadService.save_workload_for_teacher(
        uow,
        discipline_id,
        teacher_id,
        semester_number,
        saved_academic_workload
    )
