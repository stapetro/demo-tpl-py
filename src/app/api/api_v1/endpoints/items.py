"""
Items REST API
"""
from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Path, Query, status

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


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_description="List of items on success",
)
def read_items(
    skip: int = Query(  # pylint: disable=unused-argument
        default=0,
        ge=0,
        description="Number of records to skip",
    ),
    limit: int = Query(  # pylint: disable=unused-argument
        default=100,
        gt=0,
        description="Maximal number of records to return",
    ),
) -> List[schemas.Item]:
    """
    Retrieve items.
    """
    return items


@router.post("/")
def create_item(
    *,
    item_in: schemas.ItemCreate,
) -> schemas.Item:
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


@router.put(
    "/{item_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Item not found",
            "content": {"application/json": {"example": {"detail": "Item not found"}}},
        }
    },
)
def update_item(
    *,
    item_id: int = Path(
        description="Item id",
        openapi_examples={"1": {"value": 1}},
    ),
    item_in: schemas.ItemUpdate = Body(description="Item data to update"),
) -> schemas.Item:
    """
    Update an item.
    """
    item = _find_item_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id={item_id} doesn't exist",
        )
    item.title = item_in.title  # type: ignore
    item.description = item_in.description
    return item


@router.get(
    "/{item_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Item not found",
            "content": {"application/json": {"example": {"detail": "Item not found"}}},
        }
    },
)
def read_item(
    *,
    item_id: int = Path(
        description="Item id",
        openapi_examples={"1": {"value": 1}},
    ),
) -> schemas.Item:
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


@router.delete(
    "/{item_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Item not found",
            "content": {"application/json": {"example": {"detail": "Item not found"}}},
        }
    },
)
def delete_item(
    *,
    item_id: int = Path(
        description="Item id",
        openapi_examples={"1": {"value": 1}},
    ),
) -> schemas.Item:
    """
    Delete an item.
    """
    return read_item(item_id=item_id)
