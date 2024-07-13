from typing import List

from pydantic import BaseModel


class Item(BaseModel):
    item_id: str
    user_id: str
    access_token: str
    accounts: List[str]


class ItemAccess(BaseModel):
    access_token: str
    item_id: str


class ItemAccessCreate(BaseModel):
    user_id: str
    public_token: str
    public_token: str
