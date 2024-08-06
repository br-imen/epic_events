from pydantic import BaseModel, ValidationError
from decimal import Decimal

from views.contract_view import validation_error_contract_view


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


def validate_create_contract_input(**kwargs):
    try:
        user_input = ContractInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_contract_view(e)


def validate_delete_contract_input(**kwargs):
    try:
        user_input = ContractDeleteInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_contract_view(e)


def validate_update_contract_input(**kwargs):
    try:
        user_input = ContractUpdateInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_contract_view(e)
