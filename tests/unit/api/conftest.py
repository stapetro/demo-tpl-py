# pylint: disable=missing-module-docstring,missing-function-docstring
from typing import Dict

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from utils.utils import get_superuser_token_headers

from app.main import app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def api_client() -> AsyncClient:
    return new_api_client_from(app)


@pytest.fixture
def real_api_client() -> AsyncClient:
    return AsyncClient(base_url="http://localhost:8082")


@pytest.fixture(scope="module")
def superuser_token_headers() -> Dict[str, str]:
    return get_superuser_token_headers()


def new_api_client_from(app_: FastAPI) -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app_), base_url="http://test")
