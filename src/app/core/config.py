"""Defines configuration settings"""
import secrets
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, Field, PostgresDsn, validator


class Settings(BaseSettings):
    # pylint: disable=missing-class-docstring
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    VERSION: str = Field(default="0.1.0")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls, value: Union[str, List[str]]
    ) -> Union[List[str], str]:
        # pylint: disable=missing-function-docstring,no-self-argument,no-self-use
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        return value

    PROJECT_NAME: str = "dummy project"

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    PYDEVD: bool = False
    PYDEVD_PORT: Optional[int] = None
    PYDEVD_HOST: Optional[str] = None

    @validator("PROJECT_NAME")
    def get_project_name(cls, value: Optional[str], values: Dict[str, Any]) -> str:
        # pylint: disable=missing-function-docstring,no-self-argument,no-self-use
        if not value:
            return values["PROJECT_NAME"]
        return value

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(
        cls, value: bool, values: Dict[str, Any]  # pylint: disable=unused-argument
    ) -> bool:
        # pylint: disable=missing-function-docstring,no-self-argument,no-self-use
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        # pylint: disable=too-few-public-methods
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    # pylint: disable=missing-function-docstring
    return Settings()
