from typing import List

from pydantic import BaseModel


class Item(BaseModel):
    item_id: str
    user_id: str
    access_token: str
    account_ids: List[str]


class ItemAccess(BaseModel):
    item_id: str
    access_token: str


class ItemAccessCreate(BaseModel):
    user_id: str
    public_token: str
