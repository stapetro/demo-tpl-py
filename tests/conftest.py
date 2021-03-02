# pylint: disable=missing-module-docstring,missing-function-docstring
from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from utils.utils import get_superuser_token_headers

from app.main import app


@pytest.fixture(scope="module")
def api_client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers() -> Dict[str, str]:
    return get_superuser_token_headers()
