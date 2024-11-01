"""
Authentication and Authorization module
"""

import secrets
import typing as t

from fastapi import HTTPException, status
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from starlette.requests import Request

from app.core.config import get_settings

api_key_header = APIKeyHeader(name="X-API-KEY")


class ApiDocSecurity:
    """API doc security dependency"""

    def __init__(
        self,
        basic: HTTPBasic,
    ):
        self._basic = basic
        self.unauthorized_headers = (
            {"WWW-Authenticate": f'Basic realm="{self._basic.realm}"'}
            if self._basic.realm
            else {"WWW-Authenticate": "Basic"}
        )

    async def __call__(self, request: Request) -> t.Optional[str]:
        if get_settings().API_DOC_ENABLED is not True:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found",
            )
        if get_settings().ENV_NAME != "prd":
            return None
        credentials = await self._basic(request)
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers=self.unauthorized_headers,
            )
        return self._get_current_username(credentials)

    def _get_current_username(
        self,
        credentials: HTTPBasicCredentials,
    ) -> str:
        current_username_bytes = credentials.username.encode("utf8")
        correct_username_bytes = get_settings().API_DOC_USER.encode("utf8")  # type: ignore[union-attr]
        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username_bytes
        )
        current_password_bytes = credentials.password.encode("utf8")
        correct_password_bytes = (
            get_settings().API_DOC_PASSWORD.get_secret_value().encode("utf8")  # type: ignore[union-attr]
        )
        is_correct_password = secrets.compare_digest(
            current_password_bytes, correct_password_bytes
        )
        if not (is_correct_username and is_correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect authentication credentials",
                headers=self.unauthorized_headers,
            )
        return credentials.username


api_doc_security = ApiDocSecurity(basic=HTTPBasic(auto_error=True))
