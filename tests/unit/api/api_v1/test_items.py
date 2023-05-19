# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring
import pytest
from fastapi import status
from httpx import AsyncClient

from app.core.config import get_settings

pytestmark = [pytest.mark.unit, pytest.mark.anyio]


async def test_create_item(
    api_client: AsyncClient, superuser_token_headers: dict
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = await api_client.post(
        f"{get_settings().API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


async def test_read_item(
    api_client: AsyncClient, superuser_token_headers: dict
) -> None:
    item_id = 11
    response = await api_client.get(
        f"{get_settings().API_V1_STR}/items/{item_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert "title" in content
    assert "description" in content
    assert "id" in content
    assert "owner_id" in content
    assert content["id"] == item_id
