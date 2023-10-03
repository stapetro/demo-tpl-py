"""Item-related DTOs"""
from typing import Optional

from pydantic import BaseModel, ConfigDict

# pylint: disable=missing-class-docstring,too-few-public-methods


# Shared properties
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    owner_id: int
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
