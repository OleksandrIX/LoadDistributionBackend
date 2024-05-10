from enum import Enum
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    TRACE = "TRACE"


class ApplicationSettings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    model_config = SettingsConfigDict(env_file="./environments/.env.application")


class LoggerSettings(BaseSettings):
    LOG_DIR: str
    LOG_LEVEL: LogLevel
    LOG_ROTATION: str
    LOG_COMPRESSION: str

    LOG_FORMAT: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSSZZ}</green> "
        "| <level>{level:>8}</level> "
        "| <cyan>[{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}]</cyan> "
        "--- <level>{message}</level>"
    )

    @classmethod
    @field_validator("STD_LEVEL", "FILE_LEVEL")
    def validate_log_level(cls, value):
        if not isinstance(value, LogLevel):
            raise ValueError("Invalid log level")
        return value

    model_config = SettingsConfigDict(env_file="./environments/.env.logger")


class DatabaseSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="./environments/.env.database")


class MinIOSettings(BaseSettings):
    MINIO_HOST: str
    MINIO_PORT: int
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET_NAME: str
    MINIO_SECURE: bool

    @property
    def minio_url(self):
        return f"{self.MINIO_HOST}:{self.MINIO_PORT}"

    model_config = SettingsConfigDict(env_file="./environments/.env.minio")


class SecuritySettings(BaseSettings):
    ACCESS_TOKEN_EXPIRE: int
    REFRESH_TOKEN_EXPIRE: int
    ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file="./environments/.env.security")


class CorsSettings(BaseSettings):
    CORS_ALLOW_ORIGINS: str
    CORS_ALLOW_METHODS: str
    CORS_ALLOW_HEADERS: str
    CORS_ALLOW_CREDENTIALS: bool

    @property
    def allow_origins(self):
        return [origin.strip() for origin in self.CORS_ALLOW_ORIGINS.split(",") if origin.strip()]

    @property
    def allow_methods(self):
        return [method.strip() for method in self.CORS_ALLOW_METHODS.split(",") if method.strip()]

    @property
    def allow_headers(self):
        return [header.strip() for header in self.CORS_ALLOW_HEADERS.split(",") if header.strip()]

    model_config = SettingsConfigDict(env_file="./environments/.env.cors")


application_settings = ApplicationSettings()
logger_settings = LoggerSettings()
database_settings = DatabaseSettings()
minio_settings = MinIOSettings()
security_settings = SecuritySettings()
cors_settings = CorsSettings()
