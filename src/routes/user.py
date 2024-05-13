from fastapi import APIRouter, Request

from ..schemas import UserSchema, UserWithoutPasswordSchema
from ..services import UserService
from ..utils.dependencies import UOWDependencies, SecurityDependencies
from ..utils.security import JWTBearer, verify_token

router = APIRouter(
    prefix="/api/v1/users",
    tags=["User"],
    dependencies=[SecurityDependencies]
)


@router.get("/current", response_model=UserWithoutPasswordSchema, status_code=200)
async def get_current_user(request: Request, uow: UOWDependencies) -> UserWithoutPasswordSchema:
    credentials = await JWTBearer().__call__(request)
    payload = verify_token(credentials, type_token="access")
    user_id = payload.sub
    user: UserSchema = await UserService.get_user_by_id(uow, user_id)
    return UserWithoutPasswordSchema(**user.model_dump())
