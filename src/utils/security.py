from loguru import logger
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..config import security_settings
from ..schemas import TokenPayload
from ..exceptions import UnauthorizedException

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_token(subject: str, type_token: str, expires_delta: int = None) -> str:
    """
    Generates a JWT token
    :param subject: The subject of the token`
    :param type_token: The type of token (access or refresh)
    :param expires_delta: The number of seconds that the token should expire
    :return: The JWT token
    """
    if not expires_delta:
        if type_token == "access":
            expires_delta = datetime.utcnow() + timedelta(minutes=security_settings.ACCESS_TOKEN_EXPIRE)
        elif type_token == "refresh":
            expires_delta = datetime.utcnow() + timedelta(minutes=security_settings.REFRESH_TOKEN_EXPIRE)
    else:
        expires_delta = datetime.utcnow() + expires_delta

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, security_settings.JWT_SECRET_KEY, security_settings.ALGORITHM)
    return encoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self):
        super(JWTBearer, self).__init__(auto_error=False)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials:
            raise UnauthorizedException(massage="Authorization token not found.")
        if credentials.scheme != "Bearer":
            raise UnauthorizedException(massage="Invalid authentication scheme.")
        verify_token(credentials.credentials, type_token="access")
        return credentials.credentials


def verify_token(token: str, type_token: str) -> bool:
    payload = None
    try:
        if type_token == "access":
            payload = jwt.decode(token,
                                 key=security_settings.JWT_SECRET_KEY,
                                 algorithms=security_settings.ALGORITHM,
                                 options={"verify_exp": False})
        elif type_token == "refresh":
            payload = jwt.decode(token,
                                 key=security_settings.JWT_REFRESH_SECRET_KEY,
                                 algorithms=security_settings.ALGORITHM,
                                 options={"verify_exp": False})
        if payload is not None:
            token_data = TokenPayload(**payload)
            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                raise UnauthorizedException(massage="Authorization token expired.")
            return True
        return False
    except JWTError as e:
        logger.warning(e)
        raise UnauthorizedException(massage="Invalid authorization token.")
