from fastapi import APIRouter, Request

from ..schemas import DisciplineWithRelationships
from ..services import DisciplineService
from ..utils.dependencies import UOWDependencies, SecurityDependencies, AdminDependencies, AccessControlDependencies
from ..utils.security import get_current_user

router = APIRouter(
    prefix="/api/v1/disciplines",
    tags=["Disciplines"],
    dependencies=[SecurityDependencies]
)


@router.get(
    "",
    response_model=list[DisciplineWithRelationships],
    status_code=200,
)
async def get_disciplines(request: Request, uow: UOWDependencies) -> list[DisciplineWithRelationships]:
    user = await get_current_user(request, uow)
    return await DisciplineService.get_disciplines(uow, user)


@router.get(
    "/{discipline_id}",
    response_model=DisciplineWithRelationships,
    status_code=200,
    dependencies=[AccessControlDependencies]
)
async def get_discipline_by_id(uow: UOWDependencies, discipline_id: str) -> DisciplineWithRelationships:
    return await DisciplineService.get_discipline_by_id(uow, discipline_id)
