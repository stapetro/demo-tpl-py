from typing import Any, List

from fastapi import APIRouter, HTTPException

from app import schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    users = []
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = None
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = None
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
) -> Any:
    """
    Get a specific user by id.
    """
    user = None
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
