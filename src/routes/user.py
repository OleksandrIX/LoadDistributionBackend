from fastapi import APIRouter

from ..schemas import UserWithoutPasswordSchema
from ..utils.dependencies import SecurityDependencies, CurrentUserDependencies

router = APIRouter(
    prefix="/api/v1/users",
    tags=["User"],
    dependencies=[SecurityDependencies]
)


@router.get("/current", response_model=UserWithoutPasswordSchema, status_code=200)
async def get_current_user(user: CurrentUserDependencies) -> UserWithoutPasswordSchema:
    return UserWithoutPasswordSchema(**user.model_dump())
