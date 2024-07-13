from datetime import datetime
from typing import List

from pydantic import BaseModel


class Account(BaseModel):
    account_id: str
    item_id: str
    account_name: str
    balance: float
    balance_update_time: datetime
    account_type: str
    account_subtype: str
    transactions: List[str]
