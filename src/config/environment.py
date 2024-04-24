from enum import Enum
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(str, Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ApplicationSettings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    model_config = SettingsConfigDict(env_file="./environments/.env.application")


class LogggerSettings(BaseSettings):
    LOG_DIR: str
    STD_LEVEL: LogLevel
    FILE_LEVEL: LogLevel
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
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="./environments/.env.database")


application_settings = ApplicationSettings()
logger_settings = LogggerSettings()
database_settings = DatabaseSettings()
