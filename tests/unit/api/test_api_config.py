""""Test API configurations"""

# pylint: disable=missing-class-docstring,missing-function-docstring,
# pylint: disable=no-self-use

import typing as t
from unittest import mock

import pytest
from fastapi import status
from httpx import AsyncClient
from pydantic import AnyHttpUrl
from unit.api.conftest import new_api_client_from

from app.core import config
from app.main import _create_app

URL_1 = "http://localhost"
URL_2 = "http://localhost:4200"
URL_3 = "http://localhost:3000"


@pytest.mark.unit
@pytest.mark.anyio
class TestApiCors:

    @classmethod
    @pytest.fixture
    def cors_api_client(cls) -> t.Generator:
        with mock.patch(
            "app.main.get_settings",
            return_value=config.Settings(BACKEND_CORS_ORIGINS=[URL_1, URL_2, URL_3]),
        ):
            yield new_api_client_from(_create_app())

    async def test_ping__cors_allow(
        self,
        cors_api_client: AsyncClient,
    ):
        request_method = "GET"

        async with cors_api_client:
            expected_allowed_url = str(AnyHttpUrl(URL_2))
            response = await cors_api_client.options(
                f"{config.get_settings().API_V1_STR}/ping",
                headers={
                    "Access-Control-Request-Method": request_method,
                    "Origin": expected_allowed_url,
                },
            )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Access-Control-Allow-Origin"] == expected_allowed_url
        assert request_method in response.headers["Access-Control-Allow-Methods"]

    async def test_ping__cors_deny(
        self,
        cors_api_client: AsyncClient,
    ):
        request_method = "GET"

        async with cors_api_client:
            response = await cors_api_client.options(
                f"{config.get_settings().API_V1_STR}/ping",
                headers={
                    "Access-Control-Request-Method": request_method,
                    "Origin": "https://qc-ui.loc",
                },
            )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Access-Control-Allow-Origin" not in response.headers
        assert request_method in response.headers["Access-Control-Allow-Methods"]
