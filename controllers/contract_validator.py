from pydantic import BaseModel, Field, validator
from datetime import datetime, date
from typing import Optional
from decimal import Decimal

class ContractInput(BaseModel):
    id: int
    client_id: int
    commercial_contact: str
    total_amount: Decimal
    amount_due: Decimal
    status: bool

    @validator('total_amount', 'amount_due')
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError('Amount must be non-negative')
        return v

