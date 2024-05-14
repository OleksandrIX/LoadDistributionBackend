from loguru import logger
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..exceptions import (ClientException,
                          UnauthorizedException,
                          ForbiddenException,
                          NotFoundException,
                          ConflictException)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except (ClientException,
                UnauthorizedException,
                ForbiddenException,
                NotFoundException,
                ConflictException) as client_exception:
            logger.warning(client_exception.message)
            return JSONResponse(
                status_code=client_exception.status_code,
                content={"message": client_exception.message}
            )
        except HTTPException as http_exception:
            return JSONResponse(
                status_code=http_exception.status_code,
                content={"error": "Client error", "message": http_exception.detail}
            )
        except Exception as exception:
            logger.error(f"({exception.__class__.__name__}) {exception}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error", "message": "An unexpected error occurred."}
            )
