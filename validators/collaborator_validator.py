from pydantic import BaseModel, EmailStr, ValidationError, constr

from views.collaborator_view import validation_error_view


class LoginInput(BaseModel):
    """
    Represents the input data for user login.
    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The password of the user.
    """
    email: EmailStr
    password: constr()


class CollaboratorInput(BaseModel):
    """
    Represents the input data for a collaborator.
    Attributes:
        email (EmailStr): The email address of the collaborator.
        password (str): The password of the collaborator.
        employee_number (int): The employee number of the collaborator.
        name (str): The name of the collaborator.
        role_id (int): The role ID of the collaborator.
    """
    email: EmailStr
    password: constr(min_length=6)
    employee_number: int
    name: str
    role_id: int


class DeleteCollaboratorInput(BaseModel):
    """
    Represents the input data for deleting a collaborator.
    """
    employee_number: int


def validate_login_input(**kwargs):
    """
    Validates the login input.

    Args:
        **kwargs: Keyword arguments representing the login input.

    Returns:
        LoginInput: The validated login input.

    Raises:
        ValidationError: If the login input is invalid.
    """
    try:
        user_input = LoginInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_view(e)


def validate_collaborator_input(**kwargs):
    """
    Validates the input for a collaborator.

    Args:
        **kwargs: Keyword arguments representing the input fields for a collaborator.

    Returns:
        CollaboratorInput: An instance of the CollaboratorInput class if the input
        is valid.

    Raises:
        ValidationError: If the input is invalid.

    """
    try:
        user_input = CollaboratorInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_view(e)


def validate_delete_collaborator_input(**kwargs):
    """
    Validates the input for deleting a collaborator.

    Args:
        **kwargs: Keyword arguments representing the input parameters.

    Returns:
        DeleteCollaboratorInput: The validated input object.

    Raises:
        ValidationError: If the input is invalid.
    """
    try:
        user_input = DeleteCollaboratorInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_view(e)
