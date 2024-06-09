from loguru import logger
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query

from ..exceptions import ConflictException
from ..schemas import AcademicWorkloadSchema, AcademicWorkloadCreateSchema
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
    path="/disciplines/{discipline_id}",
    response_model=AcademicWorkloadSchema,
    status_code=201,
    dependencies=[AccessControlDependencies]
)
async def calculation_academic_workload(
        service: CalculationAcademicWorkloadServiceDepends,
        uow: UOWDependencies,
        discipline_id: str,
) -> AcademicWorkloadSchema:
    return await service.calculation_workload_for_discipline(
        uow=uow,
        discipline_id=discipline_id
    )


@router.get(
    path="/education-components/{education_component_id}",
    response_model=AcademicWorkloadCreateSchema,
    status_code=200,
    dependencies=[AccessControlDependencies]
)
async def calculation_academic_workload_for_education_component(
        service: CalculationAcademicWorkloadServiceDepends,
        uow: UOWDependencies,
        workload_type: str,
        education_component_id: str,
        study_group_id: Optional[str] = None
) -> AcademicWorkloadCreateSchema:
    if workload_type == "total-workload":
        return await service.calculation_workload_for_education_component(
            uow=uow,
            education_component_id=education_component_id
        )
    elif workload_type == "study-group-workload":
        return await service.calculation_group_workload(uow, education_component_id, study_group_id)
    elif workload_type == "without-lecture-workload":
        return await service.calculation_without_lecture_workload(uow, education_component_id)
    else:
        raise ConflictException(message="Unknown workload type")


@router.get(
    path="/education-components",
    response_model=AcademicWorkloadCreateSchema,
    status_code=200,
    dependencies=[AccessControlDependencies]
)
async def calculation_academic_workload_for_education_components(
        service: CalculationAcademicWorkloadServiceDepends,
        uow: UOWDependencies,
        workload_type: str,
        education_component_ids: list[str] = Query([]),
) -> AcademicWorkloadCreateSchema:
    if workload_type == "total-workload":
        return await service.calculation_academic_workload_for_education_components(
            uow=uow,
            education_component_ids=education_component_ids
        )
    elif workload_type == "lecture-workload":
        return await service.calculation_lecture_workload(uow, education_component_ids)
    else:
        raise ConflictException(message="Unknown workload type")
