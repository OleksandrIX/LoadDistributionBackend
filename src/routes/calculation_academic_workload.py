from typing import Annotated

from fastapi import APIRouter, Depends
from loguru import logger

from ..services import CalculationAcademicWorkloadService, DepartmentService
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
    path="/{department_id}",
    dependencies=[AccessControlDependencies]
)
async def calculation_academic_workload(
        department_id: str,
        service: CalculationAcademicWorkloadServiceDepends,
        uow: UOWDependencies
):
    response = []
    calculate = [
        (
            "66b21aa4-9632-4c4e-a86e-b0dd50c2e69b",
            ["4da53652-9295-4bbe-8076-0023993692c1", "1f9c0394-9f1e-46f1-9b6c-0a24c7c4180f"]
        ),
        (
            "1e6d8663-3a9c-4ba1-8612-973e72f1fcb0",
            ["760ca358-d9dd-44d4-8324-e0b86e918b31"]
        ),
        (
            "eb6b10ad-f2fa-4220-8423-40248c298719",
            ["9b14bd3c-46f8-4023-859a-d5332b6c8ca3"]
        )
    ]

    for teacher_id, disciplines_id in calculate:
        await DepartmentService.get_department_by_id(uow, department_id)
        workload = await service.calculation_classroom_workload(
            teacher_id=teacher_id,
            disciplines_id=disciplines_id,
            uow=uow
        )
        response.append(workload)

    return response
