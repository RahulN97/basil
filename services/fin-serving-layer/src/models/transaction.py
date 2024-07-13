from datetime import datetime

from pydantic import BaseModel


class Transaction(BaseModel):
    transaction_id: str
    account_id: str
    amount: float
    transaction_time: datetime
    transaction_type: str
