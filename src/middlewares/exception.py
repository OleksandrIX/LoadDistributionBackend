from loguru import logger
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..exceptions import NotFoundException, ConflictException


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except (NotFoundException, ConflictException) as client_exception:
            logger.warning(client_exception.massage)
            return JSONResponse(
                status_code=client_exception.status_code,
                content={"massage": client_exception.massage}
            )
        except HTTPException as http_exception:
            return JSONResponse(
                status_code=http_exception.status_code,
                content={"error": "Client error", "message": http_exception.detail}
            )
        except Exception as exception:
            logger.exception(f"({exception.__class__.__name__}) {exception}")
            logger.debug(type(exception))
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error", "message": "An unexpected error occurred."}
            )
