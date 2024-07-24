from pydantic import BaseModel
from decimal import Decimal


class ContractInput(BaseModel):
    client_id: int
    commercial_collaborator_id: int
    total_amount: Decimal
    amount_due: Decimal
    status: bool


class ContractUpdateInput(BaseModel):
    id: int
    client_id: int
    commercial_collaborator_id: int
    total_amount: Decimal
    amount_due: Decimal
    status: bool


class ContractDeleteInput(BaseModel):
    id: int
