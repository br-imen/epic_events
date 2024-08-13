from pydantic import BaseModel, EmailStr, ValidationError, constr

from views.collaborator_view import validation_error_view


class LoginInput(BaseModel):
    email: EmailStr
    password: constr()


class CollaboratorInput(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    employee_number: int
    name: str
    role_id: int


class DeleteCollaboratorInput(BaseModel):
    employee_number: int


def validate_login_input(**kwargs):
    try:
        user_input = LoginInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_view(e)


def validate_collaborator_input(**kwargs):
    try:
        user_input = CollaboratorInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_view(e)


def validate_delete_collaborator_input(**kwargs):
    try:
        user_input = DeleteCollaboratorInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_view(e)
