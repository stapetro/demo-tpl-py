"""
Users REST API
"""

from typing import List

from fastapi import APIRouter, Body, HTTPException, Path, Query, status

from app import schemas
from app.core.config import LoggerFactory, SomeCtx

router = APIRouter()

logger = LoggerFactory.get_logger(__name__)

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


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_description="List of users on success",
)
def read_users(
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
) -> List[schemas.User]:
    """
    Retrieve users.
    """
    logger.info("Retrieving users")
    context = SomeCtx(userId="1", geoId="geo-2")
    logger_with_ctx = LoggerFactory.wrap_logger_with_ctx(logger, context)
    logger_with_ctx.warning("Retrieving users with context")
    logger.error("Retrieving users")
    logger_with_ctx.debug("Retrieving users with context")
    logger.critical("Retrieving users")
    return users


@router.post("/")
def create_user(
    *,
    user_in: schemas.UserCreate,
) -> schemas.User:
    """
    Create a new user.
    """
    next_user_id = users[-1].id + 1  # type: ignore
    user = schemas.User(
        id=next_user_id,
        email=user_in.email,
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
        full_name=user_in.full_name,
    )
    users.append(user)
    return user


@router.get(
    "/{user_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        }
    },
)
def read_user_by_id(
    user_id: int = Path(
        description="User id",
        openapi_examples={"1": {"value": 1}},
    ),
) -> schemas.User:
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


@router.put(
    "/{user_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        }
    },
)
def update_user(
    *,
    user_id: int = Path(
        description="User id",
        openapi_examples={"1": {"value": 1}},
    ),
    user_in: schemas.UserUpdate = Body(description="User data to update"),
) -> schemas.User:
    """
    Update a user.
    """
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The user with this username does not exist in the system",
    )
