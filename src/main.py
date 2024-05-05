from fastapi import FastAPI

from .config import CustomizeLogger
from .api import all_routers
from .middlewares import ExceptionHandlerMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title="Load distribution API",
        version="0.1.0",
        docs_url="/api/v1/docs"
    )
    app.logger = CustomizeLogger.make_logger()

    app.add_middleware(ExceptionHandlerMiddleware)

    for router in all_routers:
        app.include_router(router)

    return app
