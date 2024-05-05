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


class LogggerSettings(BaseSettings):
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


application_settings = ApplicationSettings()
logger_settings = LogggerSettings()
database_settings = DatabaseSettings()
minio_settings = MinIOSettings()
