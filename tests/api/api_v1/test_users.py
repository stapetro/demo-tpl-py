from fastapi.testclient import TestClient

from app.core.config import settings
from app.schemas.user import UserCreate
from utils.utils import random_email, random_lower_string


def test_create_user_new_email(
    client: TestClient, superuser_token_headers: dict
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    assert created_user
    assert created_user["email"] == data["email"]


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user_id = 1
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    assert api_user
    assert api_user["email"] == username


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict
) -> None:
    username = random_email()
    # username = email
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item
