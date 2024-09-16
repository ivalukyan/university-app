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


class Task(BaseModel):
    id: UUID
    subject: str
    type: str
    task: str
    date: str


async def conf_date(date: str) -> str:
    dt = date.split(" ")[0].split("-")

    return f"{dt[2]}-{dt[1]}-{dt[0]}"