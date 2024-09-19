from datetime import datetime
from enum import Enum, auto
from typing import List

from pydantic import BaseModel


class AccountType(Enum):

    NOT_SPECIFIED = auto()
    INVESTMENT = auto()
    CREDIT = auto()
    DEPOSITORY = auto()
    LOAN = auto()
    BROKERAGE = auto()
    OTHER = auto()

    @classmethod
    def from_str(cls, account_type: str) -> "AccountType":
        try:
            return cls[account_type.upper()]
        except KeyError:
            return cls.NOT_SPECIFIED


class Account(BaseModel):
    account_id: str
    item_id: str
    account_name: str
    balance: float
    balance_update_time: datetime
    type: AccountType
    subtype: str
    transaction_ids: List[str]
