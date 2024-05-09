from loguru import logger
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..services import UserService
from ..schemas import UserSchema, UserLoginSchema, UserRegistrationSchema, TokenSchema
from ..utils.dependencies import UOWDependencies
from ..utils.security import verify_password, create_token

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=TokenSchema, status_code=200)
async def login(uow: UOWDependencies, login_user: UserLoginSchema) -> TokenSchema:
    user: UserSchema = await UserService.get_user_by_username(uow, login_user.username)
    if not verify_password(login_user.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user_token = TokenSchema(
        access_token=create_token(user.email, "access"),
        refresh_token=create_token(user.email, "refresh")
    )
    logger.info(f"User '{login_user.username}' with access token '{user_token.access_token}' logged in")
    return user_token


@router.post("/registration", status_code=201)
async def registration_user(uow: UOWDependencies, user: UserRegistrationSchema) -> UserSchema:
    user: UserSchema = await UserService.create_user(uow, user)
    logger.success(f"Created user with username: {user.username} and id: {user.id}")
    return user
