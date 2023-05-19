# pylint: disable=missing-module-docstring,missing-function-docstring
from typing import Dict

import pytest
from httpx import AsyncClient
from utils.utils import get_superuser_token_headers

from app.main import app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def api_client() -> AsyncClient:
    return AsyncClient(app=app, base_url="http://test")


@pytest.fixture(scope="module")
def superuser_token_headers() -> Dict[str, str]:
    return get_superuser_token_headers()
