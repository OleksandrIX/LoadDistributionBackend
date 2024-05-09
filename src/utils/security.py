from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt, JWTError
from typing import Union, Any
from datetime import datetime, timedelta
from passlib.context import CryptContext

from ..config import security_settings
from ..schemas import TokenPayload

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_token(subject: Union[str, Any], type_token: str, expires_delta: int = None) -> str:
    """
    Generates a JWT token
    :param subject: The subject of the token
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


security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, security_settings.JWT_SECRET_KEY, algorithms=security_settings.ALGORITHM)
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=401,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
