from pydantic import BaseModel, ValidationError
from decimal import Decimal

from views.contract_view import validation_error_contract_view


class ContractInput(BaseModel):
    """
    Represents the input data for a contract.
    Attributes:
        client_id (int): The ID of the client.
        total_amount (Decimal): The total amount of the contract.
        amount_due (Decimal): The amount due for the contract.
        status (bool): The status of the contract.
    """

    client_id: int
    total_amount: Decimal
    amount_due: Decimal
    status: bool


class ContractUpdateInput(BaseModel):
    """
    Represents the input data for updating a contract.
    Attributes:
        id (int): The ID of the contract.
        client_id (int): The ID of the client associated with the contract.
        commercial_collaborator_id (int): The ID of the commercial collaborator
        associated with the contract.
        total_amount (Decimal): The total amount of the contract.
        amount_due (Decimal): The amount due for the contract.
        status (bool): The status of the contract.
    """

    id: int
    client_id: int
    total_amount: Decimal
    amount_due: Decimal
    status: bool


class ContractDeleteInput(BaseModel):
    """
    Represents the input data for deleting a contract.
    Attributes:
        id (int): The ID of the contract to be deleted.
    """
    id: int


def validate_create_contract_input(**kwargs):
    """
    Validates the input for creating a contract.

    Args:
        **kwargs: Keyword arguments representing the contract input fields.

    Returns:
        ContractInput: The validated contract input.

    Raises:
        ValidationError: If the input fails validation.

    """
    try:
        user_input = ContractInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_contract_view(e)


def validate_delete_contract_input(**kwargs):
    """
    Validates the input for deleting a contract.

    Args:
        **kwargs: Keyword arguments representing the input parameters for
        deleting a contract.

    Returns:
        ContractDeleteInput: The validated input for deleting a contract.

    Raises:
        ValidationError: If the input parameters are invalid.
    """
    try:
        user_input = ContractDeleteInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_contract_view(e)


def validate_update_contract_input(**kwargs):
    """
    Validates the input for updating a contract.

    Args:
        **kwargs: Keyword arguments representing the contract update input.

    Returns:
        ContractUpdateInput: The validated contract update input.

    Raises:
        ValidationError: If the input is invalid.
    """
    try:
        user_input = ContractUpdateInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_contract_view(e)
