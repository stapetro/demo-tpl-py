"""
Users REST API
"""
from typing import Any, List

from fastapi import APIRouter, HTTPException, status

from app import schemas

router = APIRouter()

users = [
    schemas.User(
        id=1,
        email="martin.fowler@geeky.eu",
        is_active=True,
        is_superuser=True,
        full_name="Martin Fowler",
    ),
    schemas.User(
        id=2,
        email="uncle.bob@geeky.eu",
        is_active=False,
        is_superuser=True,
        full_name="Uncle Bob",
    ),
]


@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    next_user_id = users[-1].id + 1
    user = schemas.User(
        id=next_user_id,
        email=user_in.email,
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
        full_name=user_in.full_name,
    )
    users.append(user)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
) -> Any:
    """
    Get a specific user by id.
    """
    user = next((usr for usr in users if usr.id == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} doesn't exist",
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    user_id: int,
    user_in: schemas.UserUpdate,
) -> Any:
    """
    Update a user.
    """
    raise HTTPException(
        status_code=404,
        detail="The user with this username does not exist in the system",
    )
