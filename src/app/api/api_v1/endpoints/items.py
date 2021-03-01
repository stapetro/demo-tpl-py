from typing import Any, List

from fastapi import APIRouter

from app import schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve items.
    """
    items = []
    return items


@router.post("/", response_model=schemas.Item)
def create_item(
    *,
    item_in: schemas.ItemCreate,
) -> Any:
    """
    Create new item.
    """
    item = None
    return item


@router.put("/{id}", response_model=schemas.Item)
def update_item(
    *,
    id: int,
    item_in: schemas.ItemUpdate,
) -> Any:
    """
    Update an item.
    """
    item = None
    return item


@router.get("/{id}", response_model=schemas.Item)
def read_item(
    *,
    id: int,
) -> Any:
    """
    Get item by ID.
    """
    item = None
    return item


@router.delete("/{id}", response_model=schemas.Item)
def delete_item(
    *,
    id: int,
) -> Any:
    """
    Delete an item.
    """
    item = None
    return item
