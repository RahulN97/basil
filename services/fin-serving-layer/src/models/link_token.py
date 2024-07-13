from pydantic import BaseModel


class LinkToken(BaseModel):
    token: str


class LinkTokenCreate(BaseModel):
    user_id: str
    institution_type: str
