from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    name: str
    email: str
    creation_time: datetime
    update_time: datetime


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
