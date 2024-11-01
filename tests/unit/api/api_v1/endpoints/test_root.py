# pylint: disable=missing-module-docstring,missing-function-docstring,
# pylint: disable=missing-class-docstring,no-self-use
from unittest import mock

import pytest
from fastapi import status
from httpx import AsyncClient
from pydantic import SecretStr

from app.core.config import get_settings

pytestmark = pytest.mark.unit


@pytest.mark.anyio
class TestRoot:
    @pytest.mark.parametrize(
        "url_path,expected_status_code",
        [
            (f"{get_settings().API_V1_STR}/", status.HTTP_404_NOT_FOUND),
            ("/swagger", status.HTTP_404_NOT_FOUND),
            ("/redoc", status.HTTP_404_NOT_FOUND),
            ("/openapi.json", status.HTTP_404_NOT_FOUND),
        ],
    )
    async def test_path__protected(
        self,
        api_client: AsyncClient,
        url_path: str,
        expected_status_code: int,
    ) -> None:
        async with api_client:
            response = await api_client.get(url_path)

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "url_path",
        [
            "/swagger",
            "/redoc",
            "/openapi.json",
        ],
    )
    @pytest.mark.parametrize(
        "env_name,expected_status_code",
        [
            ("tst-loc", status.HTTP_200_OK),
            ("prd", status.HTTP_401_UNAUTHORIZED),
        ],
    )
    async def test_doc_path__protected_by_env(
        self,
        api_client: AsyncClient,
        url_path: str,
        env_name: str,
        expected_status_code: int,
    ):
        with mock.patch("app.api.api_v1.auth.get_settings") as mock_get_settings:
            mock_get_settings.return_value = mock.Mock(
                API_DOC_ENABLED=True, ENV_NAME=env_name
            )
            async with api_client:
                response = await api_client.get(url_path)

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "url_path",
        [
            "/swagger",
            "/redoc",
            "/openapi.json",
        ],
    )
    @pytest.mark.parametrize(
        "user_name,user_pwd",
        [
            ("dummy1", "dummy2"),
            ("my_user", "dummy3"),
            ("dummy4", "password123"),
        ],
    )
    async def test_doc_path__aut_invalid_creds(
        self,
        api_client: AsyncClient,
        url_path: str,
        user_name: str,
        user_pwd: str,
    ):
        with mock.patch("app.api.api_v1.auth.get_settings") as mock_get_settings:
            api_doc_user = "my_user"
            api_doc_pwd = SecretStr("password123")
            mock_get_settings.return_value = mock.Mock(
                ENV_NAME="prd",
                API_DOC_ENABLED=True,
                API_DOC_USER=api_doc_user,
                API_DOC_PASSWORD=api_doc_pwd,
            )
            async with api_client:
                response = await api_client.get(url_path, auth=(user_name, user_pwd))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "url_path",
        [
            "/swagger",
            "/redoc",
            "/openapi.json",
        ],
    )
    @pytest.mark.parametrize(
        "env_name",
        ["tst-loc", "prd"],
    )
    async def test_doc_path__disabled_api_doc(
        self,
        api_client: AsyncClient,
        url_path: str,
        env_name: str,
    ):
        with mock.patch("app.api.api_v1.auth.get_settings") as mock_get_settings:
            mock_get_settings.return_value = mock.Mock(
                API_DOC_ENABLED=False, ENV_NAME=env_name
            )
            async with api_client:
                response = await api_client.get(url_path)

        assert response.status_code == status.HTTP_404_NOT_FOUND
