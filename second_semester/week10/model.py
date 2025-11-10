from typing import Optional

from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    description: str
    is_done: bool = False


class TodoItem(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None

