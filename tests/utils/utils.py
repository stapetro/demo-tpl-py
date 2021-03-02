"""Common utilities for all types of tests"""
# pylint: disable=missing-function-docstring
import random
import string
from datetime import timedelta
from typing import Dict

from fastapi.testclient import TestClient

from app.core import security
from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_superuser_token_headers() -> Dict[str, str]:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    user_id = -1
    a_token = security.create_access_token(user_id, expires_delta=access_token_expires)
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
