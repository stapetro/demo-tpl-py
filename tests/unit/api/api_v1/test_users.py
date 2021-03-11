# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,no-self-use
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from utils.utils import random_email, random_lower_string

from app.core.config import settings


@pytest.mark.unit
class TestUsersApi:
    def test_create_user_new_email(
        self, api_client, superuser_token_headers: dict
    ) -> None:
        username = random_email()
        password = random_lower_string()
        data = {"email": username, "password": password}
        response = api_client.post(
            f"{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=data,
        )
        assert 200 <= response.status_code < 300
        created_user = response.json()
        assert created_user
        assert created_user["email"] == data["email"]

    def test_get_existing_user(self, api_client, superuser_token_headers: dict) -> None:
        user_id = 1
        r = api_client.get(
            f"{settings.API_V1_STR}/users/{user_id}",
            headers=superuser_token_headers,
        )
        assert 200 <= r.status_code < 300
        api_user = r.json()
        assert api_user
        assert "email" in api_user

    def test_get_non_existing_user(
        self, api_client, superuser_token_headers: dict
    ) -> None:
        user_id = -99
        response = api_client.get(
            f"{settings.API_V1_STR}/users/{user_id}",
            headers=superuser_token_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_users(self, api_client, superuser_token_headers: dict) -> None:
        response = api_client.get(
            f"{settings.API_V1_STR}/users/", headers=superuser_token_headers
        )
        all_users = response.json()

        assert len(all_users) > 1
        for item in all_users:
            assert "email" in item
