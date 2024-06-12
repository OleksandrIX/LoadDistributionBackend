from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check

from .config import CustomizeLogger, application_settings
from .middlewares import ExceptionHandlerMiddleware, CorsMiddleware
from .routes import all_routers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Load distribution API",
        version=application_settings.APP_VERSION,
        docs_url="/api/v1/docs"
    )
    app.logger = CustomizeLogger.make_logger()

    add_pagination(app)
    app.add_middleware(ExceptionHandlerMiddleware)
    app.add_middleware(CorsMiddleware)

    for router in all_routers:
        app.include_router(router)

    disable_installed_extensions_check()

    return app
