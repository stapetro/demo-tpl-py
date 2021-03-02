# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings


@pytest.mark.unit
def test_create_item(api_client, superuser_token_headers: dict) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = api_client.post(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


@pytest.mark.unit
def test_read_item(api_client, superuser_token_headers: dict) -> None:
    item_id = 11
    response = api_client.get(
        f"{settings.API_V1_STR}/items/{item_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert "title" in content
    assert "description" in content
    assert "id" in content
    assert "owner_id" in content
    assert content["id"] == item_id
