"""Token DTOs"""
from typing import Optional

from pydantic import BaseModel

# pylint: disable=missing-class-docstring


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
