# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,no-self-use
import pytest
from fastapi import status
from httpx import AsyncClient
from utils.utils import random_email, random_lower_string

from app.core.config import get_settings

pytestmark = [pytest.mark.unit, pytest.mark.anyio]


class TestUsersApi:
    async def test_create_user_new_email(
        self, api_client: AsyncClient, superuser_token_headers: dict
    ) -> None:
        username = random_email()
        password = random_lower_string()
        data = {"email": username, "password": password}
        response = await api_client.post(
            f"{get_settings().API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=data,
        )
        assert 200 <= response.status_code < 300
        created_user = response.json()
        assert created_user
        assert created_user["email"] == data["email"]

    async def test_get_existing_user(
        self, api_client: AsyncClient, superuser_token_headers: dict
    ) -> None:
        user_id = 1
        response = await api_client.get(
            f"{get_settings().API_V1_STR}/users/{user_id}",
            headers=superuser_token_headers,
        )
        assert 200 <= response.status_code < 300
        api_user = response.json()
        assert api_user
        assert "email" in api_user

    async def test_get_non_existing_user(
        self, api_client: AsyncClient, superuser_token_headers: dict
    ) -> None:
        user_id = -99
        response = await api_client.get(
            f"{get_settings().API_V1_STR}/users/{user_id}",
            headers=superuser_token_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_retrieve_users(
        self, api_client: AsyncClient, superuser_token_headers: dict
    ) -> None:
        response = await api_client.get(
            f"{get_settings().API_V1_STR}/users/", headers=superuser_token_headers
        )
        all_users = response.json()

        assert len(all_users) > 1
        for item in all_users:
            assert "email" in item
