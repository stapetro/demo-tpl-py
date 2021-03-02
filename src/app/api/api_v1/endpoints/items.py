"""
Items REST API
"""
from typing import Any, List, Optional

from fastapi import APIRouter, HTTPException, status

from app import schemas

router = APIRouter()

items: List[schemas.Item] = [
    schemas.Item(
        id=11,
        title="Pythoneer",
        description="I'd like to be Pythoneer instead of Pythonista",
        owner_id=1,
    ),
    schemas.Item(
        id=12,
        title="Pythonista",
        description="Pythonista is not that bad at the beginning",
        owner_id=2,
    ),
]


@router.get("/", response_model=List[schemas.Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve items.
    """
    return items


@router.post("/", response_model=schemas.Item)
def create_item(
    *,
    item_in: schemas.ItemCreate,
) -> Any:
    """
    Create new item.
    """
    next_item_id = items[-1].id + 1  # pylint: disable=no-member
    item = schemas.Item(
        id=next_item_id,
        title=item_in.title,
        description=item_in.description,
        owner_id=2,
    )
    items.append(item)
    return item


@router.put("/{item_id}", response_model=schemas.Item)
def update_item(
    *,
    item_id: int,
    item_in: schemas.ItemUpdate,
) -> Any:
    """
    Update an item.
    """
    item = _find_item_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id={item_id} doesn't exist",
        )
    item.title = item_in.title
    item.description = item_in.description
    return item


@router.get("/{item_id}", response_model=schemas.Item)
def read_item(
    *,
    item_id: int,
) -> Any:
    """
    Get item by ID.
    """
    item = _find_item_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id={item_id} doesn't exist",
        )
    return item


def _find_item_by_id(item_id: int) -> Optional[schemas.Item]:
    # pylint: disable=no-member
    return next((itm for itm in items if itm.id == item_id), None)


@router.delete("/{item_id}", response_model=schemas.Item)
def delete_item(
    *,
    item_id: int,
) -> Any:
    """
    Delete an item.
    """
    return read_item(item_id=item_id)
