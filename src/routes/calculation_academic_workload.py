from typing import Annotated

from fastapi import APIRouter, Depends

from ..schemas import AcademicWorkloadSchema
from ..services import CalculationAcademicWorkloadService
from ..utils.dependencies import UOWDependencies, SecurityDependencies, AccessControlDependencies

CalculationAcademicWorkloadServiceDepends = Annotated[
    CalculationAcademicWorkloadService,
    Depends(CalculationAcademicWorkloadService)
]

router = APIRouter(
    prefix="/api/v1/calculation-academic-workload",
    tags=["Calculation academic workload"],
    dependencies=[SecurityDependencies]
)


@router.get(
    path="",
    response_model=AcademicWorkloadSchema,
    status_code=201,
    dependencies=[AccessControlDependencies]
)
async def calculation_academic_workload(
        service: CalculationAcademicWorkloadServiceDepends,
        uow: UOWDependencies,
        discipline_id: str,
) -> AcademicWorkloadSchema:
    return await service.calculation_workload_for_discipline(uow=uow, discipline_id=discipline_id)
