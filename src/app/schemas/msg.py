"""Message DTOs"""

from pydantic import BaseModel

# pylint: disable=missing-class-docstring


class Msg(BaseModel):
    msg: str
