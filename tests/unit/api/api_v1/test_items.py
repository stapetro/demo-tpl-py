import pytest
from fastapi.testclient import TestClient

from app.core.config import settings


@pytest.mark.unit
def test_create_item(client: TestClient, superuser_token_headers: dict) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


@pytest.mark.unit
def test_read_item(client: TestClient, superuser_token_headers: dict) -> None:
    item_id = 1
    response = client.get(
        f"{settings.API_V1_STR}/items/{item_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "title" in content
    # assert content["title"] == item.title
    # assert content["description"] == item.description
    # assert content["id"] == item.id
    # assert content["owner_id"] == item.owner_id
