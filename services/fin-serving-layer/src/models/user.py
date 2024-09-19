from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    name: str
    email: str
    creation_time: datetime
    update_time: datetime
    item_ids: List[str]


class BaseUserRequest(BaseModel):
    user_id: str


class UserGet(BaseUserRequest):
    pass


class UserCreate(BaseUserRequest):
    name: str
    email: str


class UserUpdate(BaseUserRequest):
    name: Optional[str]
    email: Optional[str]


class UserDelete(BaseUserRequest):
    pass
