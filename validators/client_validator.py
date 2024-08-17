from pydantic import BaseModel, EmailStr, ValidationError

from views.client_view import validation_error_client_view


class ClientInput(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    company_name: str
    commercial_collaborator_id: str


class ClientInputUpdate(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone_number: str
    company_name: str
    commercial_collaborator_id: str


class ClientDeleteInput(BaseModel):
    client_id: int


def validate_create_client(**kwargs):
    """
    Validates the input for creating a client.

    Args:
        **kwargs: Keyword arguments representing the client input.

    Returns:
        ClientInput: The validated client input.

    Raises:
        ValidationError: If the input is invalid.
    """
    try:
        user_input = ClientInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_client_view(e)


def validate_delete_client_input(**kwargs):
    """
    Validates the input for deleting a client.

    Args:
        **kwargs: Keyword arguments representing the input parameters.

    Returns:
        ClientDeleteInput: The validated input for deleting a client.

    Raises:
        ValidationError: If the input is invalid.
    """
    try:
        user_input = ClientDeleteInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_client_view(e)


def validate_update_client(**kwargs):
    """
    Validates the input for updating a client.

    Args:
        **kwargs: Keyword arguments containing the input data for updating a client.

    Returns:
        ClientInputUpdate: An instance of the ClientInputUpdate class representing
        the validated input.

    Raises:
        ValidationError: If the input data fails validation.

    """
    try:
        user_input = ClientInputUpdate(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_client_view(e)
