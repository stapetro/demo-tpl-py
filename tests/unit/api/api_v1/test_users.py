import pytest
from fastapi import status
from fastapi.testclient import TestClient
from utils.utils import random_email, random_lower_string

from app.core.config import settings


@pytest.mark.unit
class TestUsersApi:
    def test_create_user_new_email(
        self, client: TestClient, superuser_token_headers: dict
    ) -> None:
        username = random_email()
        password = random_lower_string()
        data = {"email": username, "password": password}
        r = client.post(
            f"{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=data,
        )
        assert 200 <= r.status_code < 300
        created_user = r.json()
        assert created_user
        assert created_user["email"] == data["email"]

    def test_get_existing_user(
        self, client: TestClient, superuser_token_headers: dict
    ) -> None:
        user_id = 1
        r = client.get(
            f"{settings.API_V1_STR}/users/{user_id}",
            headers=superuser_token_headers,
        )
        assert 200 <= r.status_code < 300
        api_user = r.json()
        assert api_user
        assert "email" in api_user

    def test_get_non_existing_user(
        self, client: TestClient, superuser_token_headers: dict
    ) -> None:
        user_id = -99
        r = client.get(
            f"{settings.API_V1_STR}/users/{user_id}",
            headers=superuser_token_headers,
        )
        assert r.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_users(
        self, client: TestClient, superuser_token_headers: dict
    ) -> None:
        r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
        all_users = r.json()

        assert len(all_users) > 1
        for item in all_users:
            assert "email" in item
