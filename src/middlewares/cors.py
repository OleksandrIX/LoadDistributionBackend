from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..config import cors_settings


class CorsMiddleware(CORSMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(
            app=app,
            allow_origins=cors_settings.allow_origins,
            allow_methods=cors_settings.allow_methods,
            allow_headers=cors_settings.allow_headers,
            allow_credentials=cors_settings.CORS_ALLOW_CREDENTIALS
        )
