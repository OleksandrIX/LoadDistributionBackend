from typing import Annotated

from fastapi import APIRouter, Depends

from ..services import DepartmentService, AcademicDistributionService
from ..utils.dependencies import UOWDependencies, SecurityDependencies, CurrentUserDependencies

AcademicDistributionServiceDependencies = Annotated[AcademicDistributionService, Depends(AcademicDistributionService)]

router = APIRouter(
    prefix="/api/v1/academic-distribution-sessions",
    tags=["Academic Workload"],
    dependencies=[SecurityDependencies]
)


@router.get(
    path="",
    response_model=None,
    status_code=200
)
async def get_all_distribution_sessions(
        uow: UOWDependencies,
        user: CurrentUserDependencies,
        distribution_service: AcademicDistributionServiceDependencies,
):
    department = await DepartmentService.get_department_by_id(uow, user.department_id)
    return await distribution_service.get_all_sessions(department.department_code)


@router.get(
    path="/{distribution_name}",
    response_model=None,
    status_code=200
)
async def get_distribution_session(
        uow: UOWDependencies,
        user: CurrentUserDependencies,
        distribution_service: AcademicDistributionServiceDependencies,
        distribution_name: str,
):
    department = await DepartmentService.get_department_by_id(uow, user.department_id)
    return await distribution_service.get_session(department.department_code, distribution_name)


@router.post(
    path="",
    response_model=None,
    status_code=204,
)
async def created_distribution_session(
        uow: UOWDependencies,
        user: CurrentUserDependencies,
        distribution_service: AcademicDistributionServiceDependencies,
        session_data: dict,
):
    department = await DepartmentService.get_department_by_id(uow, user.department_id)
    await distribution_service.save_session(department.department_code, session_data)


@router.delete(
    path="/{distribution_name}",
    response_model=None,
    status_code=204
)
async def delete_distribution_session(
        uow: UOWDependencies,
        user: CurrentUserDependencies,
        distribution_service: AcademicDistributionServiceDependencies,
        distribution_name: str,
):
    department = await DepartmentService.get_department_by_id(uow, user.department_id)
    await distribution_service.delete_session(department.department_code, distribution_name)
