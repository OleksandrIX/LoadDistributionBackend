from fastapi import APIRouter
from fastapi import Request, Response
from loguru import logger

from ..config import security_settings
from ..exceptions import ClientException, UnauthorizedException
from ..schemas import (UserSchema,
                       UserWithoutPasswordSchema,
                       UserLoginSchema,
                       UserRegistrationSchema,
                       TokenSchema,
                       TokenPayloadSchema)
from ..services import UserService
from ..utils.dependencies import UOWDependencies
from ..utils.security import verify_password, create_token, verify_token

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post("/registration", response_model=UserWithoutPasswordSchema, status_code=201)
async def registration_user(uow: UOWDependencies, user: UserRegistrationSchema) -> UserWithoutPasswordSchema:
    user: UserSchema = await UserService.create_user(uow, user)
    logger.success(f"Created user with id '{user.id}'")
    return UserWithoutPasswordSchema(**user.model_dump())


@router.post(
    path="/login",
    status_code=200,
    response_model=TokenSchema,
    response_description="Created in the cookies refresh_token and logged_in"
)
async def login(response: Response, uow: UOWDependencies, login_user: UserLoginSchema) -> TokenSchema:
    user: UserSchema = await UserService.get_user_by_username(uow, login_user.username)
    if not verify_password(login_user.password, user.password):
        raise ClientException(status_code=400, message="Incorrect password")
    access_token = create_token(user.id, "access")
    refresh_token = create_token(user.id, "refresh")
    response.set_cookie("refresh_token", refresh_token,
                        security_settings.REFRESH_TOKEN_EXPIRE * 60,
                        security_settings.REFRESH_TOKEN_EXPIRE * 60,
                        "/", None, True, True, "lax")
    response.set_cookie("logged_in", "True",
                        security_settings.ACCESS_TOKEN_EXPIRE * 60,
                        security_settings.ACCESS_TOKEN_EXPIRE * 60,
                        "/", None, True, True, "lax")
    logger.info(f"User '{user.id}' logged in")
    return TokenSchema(access_token=access_token)


@router.post(
    "/refresh",
    status_code=200,
    response_model=TokenSchema,
    response_description="Updated in the cookies logged_in and return access token"
)
async def refresh_token(request: Request, response: Response, uow: UOWDependencies) -> TokenSchema:
    refresh_token = request.cookies.get("refresh_token")
    token_payload: TokenPayloadSchema = verify_token(refresh_token, "refresh")
    user: UserSchema = await UserService.get_user_by_id(uow, token_payload.sub)
    access_token = create_token(user.id, "access")
    response.set_cookie("logged_in", "True",
                        security_settings.ACCESS_TOKEN_EXPIRE * 60,
                        security_settings.ACCESS_TOKEN_EXPIRE * 60,
                        "/", None, True, True, "lax")
    return TokenSchema(access_token=access_token)


@router.delete(
    path="/logout",
    status_code=204,
    response_description="Deleted from the cookies refresh_token and logged_in"
)
async def logout(response: Response):
    response.delete_cookie("logged_in")
    response.delete_cookie("refresh_token")
