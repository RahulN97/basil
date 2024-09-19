from datetime import datetime
from enum import Enum, auto

from pydantic import BaseModel


class TransactionType(Enum):

    NOT_SPECIFIED = auto()
    ONLINE = auto()
    IN_STORE = auto()
    OTHER = auto()

    @classmethod
    def from_str(cls, transaction_type: str) -> "TransactionType":
        try:
            return cls[transaction_type.upper().replace(" ", "_")]
        except KeyError:
            return cls.NOT_SPECIFIED


class TransactionBase(BaseModel):
    transaction_id: str
    account_id: str


class Transaction(TransactionBase):
    amount: float
    transaction_time: datetime
    type: TransactionType


class RemovedTransaction(TransactionBase):
    pass
