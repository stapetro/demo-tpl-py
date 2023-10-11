"""Defines configuration settings"""
import logging
import secrets
import typing as t
from functools import lru_cache

import ecs_logging
import uvicorn
from pydantic import (
    AnyHttpUrl,
    BaseModel,
    EmailStr,
    Field,
    PostgresDsn,
    field_validator,
)
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # pylint: disable=missing-class-docstring
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: t.List[AnyHttpUrl] = []
    VERSION: str = Field(default="0.1.0")

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(
        cls, value: t.Union[str, t.List[str]]
    ) -> t.Union[t.List[str], str]:
        # pylint: disable=missing-function-docstring,no-self-argument,no-self-use
        if isinstance(value, str):
            return [value]
        return value

    PROJECT_NAME: str = "dummy project"
    ENV_NAME: str = "dummy env"

    SQLALCHEMY_DATABASE_URI: t.Optional[PostgresDsn] = None

    SMTP_TLS: bool = True
    SMTP_PORT: t.Optional[int] = None
    SMTP_HOST: t.Optional[str] = None
    SMTP_USER: t.Optional[str] = None
    SMTP_PASSWORD: t.Optional[str] = None
    EMAILS_FROM_EMAIL: t.Optional[EmailStr] = None
    EMAILS_FROM_NAME: t.Optional[str] = None
    PYDEVD: bool = False
    PYDEVD_PORT: t.Optional[int] = None
    PYDEVD_HOST: t.Optional[str] = None

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @field_validator("EMAILS_ENABLED", mode="before")
    def get_emails_enabled(
        cls,
        value: bool,  # pylint: disable=unused-argument
        info: ValidationInfo,
    ) -> bool:
        # pylint: disable=missing-function-docstring,no-self-argument,no-self-use
        values = getattr(info, "data")
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    USERS_OPEN_REGISTRATION: bool = False
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", env_file_encoding="utf-8"
    )


class AccessEcsLogFormatter(ecs_logging.StdlibFormatter):
    """ECS Formatter for uvicorn.access logger"""

    def format_to_ecs(self, record: logging.LogRecord) -> dict[str, t.Any]:
        (
            client_addr,
            method,
            full_path,
            http_version,
            status_code,
        ) = record.args  # type: ignore[misc]
        if self._extra is None:
            self._extra = {}
        self._extra.update(
            {
                "client.address": client_addr,
                "http.response.status_code": int(status_code),  # type: ignore[arg-type]
                "http.request.method": method,
                "http.version": http_version,
                "url.path": full_path,
            }
        )
        return super().format_to_ecs(record)


class LoggingConfig:
    """Logging configuration"""

    ECS_UVICORN_LOGGING_CONFIG = {
        **uvicorn.config.LOGGING_CONFIG,
        "formatters": {
            "ecs": {
                "()": "ecs_logging.StdlibFormatter",
            },
            "ecs_access": {
                "()": "app.core.config.AccessEcsLogFormatter",
            },
        },
        "handlers": {
            "default": {
                "formatter": "ecs",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "ecs_access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
    }

    @classmethod
    def get_config(cls, env_name: str) -> dict:
        """
        Returns logging configuration for the given environment.
        :param env_name: Environment name
        :return: Logging configuration
        """
        if env_name == "loc":
            return uvicorn.config.LOGGING_CONFIG
        return cls.ECS_UVICORN_LOGGING_CONFIG


class SomeCtx(BaseModel):
    userId: str
    geoId: str


class LoggerFactory:
    """Logger factory"""

    @classmethod
    def wrap_logger_with_ctx(
        cls,
        logger: logging.Logger | logging.LoggerAdapter,
        mdc: SomeCtx | None = None,
    ) -> logging.Logger:
        """
        Wraps existing logger with context.
        :param logger: Logger instance
        :param mdc: Message Diagnostic Context
        :return: Logger enriched with the provided context
        """
        labels = cls._convert_some_ctx_to_labels(mdc)
        # https://stackoverflow.com/q/45292635/7970759
        if isinstance(logger, logging.LoggerAdapter):
            logger.extra["labels"] = labels  # type: ignore[index]
            return logger  # type: ignore[return-value]
        logger = logging.LoggerAdapter(
            logger,  # type: ignore[assignment]
            extra={"labels": labels},
        )
        return logger  # type: ignore[return-value]

    @classmethod
    def get_logger(
        cls,
        name: str,
        mdc: SomeCtx | None = None,
    ) -> logging.Logger:
        """
        Creates and returns a logger with context.
        :param name: Logger name
        :param mdc: Message Diagnostic Context
        :return: Logger enriched with the provided context
        """
        return cls.wrap_logger_with_ctx(logging.getLogger(name), mdc)

    @classmethod
    def _convert_some_ctx_to_labels(cls, mdc: SomeCtx | None) -> dict[str, t.Any]:
        if mdc is None:
            return {}
        return {
            "userId": mdc.userId,
            "geoId": mdc.geoId,
        }


@lru_cache()
def get_settings() -> Settings:
    # pylint: disable=missing-function-docstring
    return Settings()
