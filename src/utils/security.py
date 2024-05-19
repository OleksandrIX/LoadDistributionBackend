from datetime import datetime, timedelta

from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext

from .schema import RoleEnum
from .unit_of_work import IUnitOfWork, UnitOfWork
from ..config import security_settings
from ..exceptions import UnauthorizedException, ForbiddenException
from ..schemas import TokenPayloadSchema, UserSchema

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def encode_token(subject: str, type_token: str) -> str:
    if type_token == "access":
        expires_delta = datetime.utcnow() + timedelta(minutes=security_settings.ACCESS_TOKEN_EXPIRE)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        return jwt.encode(claims=to_encode,
                          key=security_settings.JWT_SECRET_KEY,
                          algorithm=security_settings.ALGORITHM)
    elif type_token == "refresh":
        expires_delta = datetime.utcnow() + timedelta(minutes=security_settings.REFRESH_TOKEN_EXPIRE)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        return jwt.encode(claims=to_encode,
                          key=security_settings.JWT_REFRESH_SECRET_KEY,
                          algorithm=security_settings.ALGORITHM)
    else:
        raise UnauthorizedException(message="Invalid type token.")


def decode_token(token: str, type_token: str, options: dict) -> dict:
    if type_token == "access":
        return jwt.decode(token=token,
                          key=security_settings.JWT_SECRET_KEY,
                          algorithms=security_settings.ALGORITHM,
                          options=options)
    elif type_token == "refresh":
        return jwt.decode(token=token,
                          key=security_settings.JWT_REFRESH_SECRET_KEY,
                          algorithms=security_settings.ALGORITHM,
                          options=options)
    else:
        raise UnauthorizedException(message="Invalid type token.")


def create_token(subject: str, type_token: str) -> str:
    """
    Generates a JWT token
    :param subject: The subject of the token`
    :param type_token: The type of token (access or refresh)
    :return: The JWT token
    """
    return encode_token(subject, type_token)


def verify_token(token: str, type_token: str) -> TokenPayloadSchema:
    """
        Verification a JWT token
        :param token: The JWT token to verify
        :param type_token: The type of token (access or refresh)
        :return: True if the token is valid, False otherwise
        """
    try:
        payload = decode_token(token, type_token, options={"verify_exp": False})
        token_payload = TokenPayloadSchema(**payload)
        if datetime.fromtimestamp(token_payload.exp) < datetime.now():
            raise UnauthorizedException(message="Authorization token expired.")
        return token_payload
    except JWTError as err:
        raise UnauthorizedException(message=str(err))


async def get_user_id_from_token(request: Request) -> str:
    credentials = await JWTBearer().__call__(request)
    payload = verify_token(credentials, type_token="access")
    user_id = payload.sub
    return user_id


async def get_current_user(request: Request, uow: IUnitOfWork = Depends(UnitOfWork)) -> UserSchema:
    from ..services import UserService
    user_id = await get_user_id_from_token(request)
    return await UserService.get_user_by_id(uow, user_id)


async def check_is_admin(request: Request, uow: IUnitOfWork = Depends(UnitOfWork)) -> bool:
    user: UserSchema = await get_current_user(request, uow)
    if user.role == RoleEnum.admin:
        return user.department_id
    elif user.role == RoleEnum.user:
        raise ForbiddenException(message="User is not an administrator")
    else:
        raise ForbiddenException(message="Unknown role of the user")


class JWTBearer(HTTPBearer):
    def __init__(self):
        super(JWTBearer, self).__init__(auto_error=False)

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials:
            raise UnauthorizedException(message="Authorization token not found.")
        if credentials.scheme != "Bearer":
            raise UnauthorizedException(message="Invalid authentication scheme.")
        verify_token(credentials.credentials, type_token="access")
        return credentials.credentials
