"""
Utils module
"""

from pydantic import BaseModel
from pydantic.types import UUID


class User(BaseModel):
    id: UUID
    fullname: str
    telegram_id: int
    auth: bool
    superuser: bool