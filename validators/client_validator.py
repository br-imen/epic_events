from pydantic import BaseModel, EmailStr, ValidationError

from views.client_view import validation_error_client_view



class ClientInput(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    company_name: str
    commercial_collaborator_id: str

class ClientInputUpdate(BaseModel):
    id : int
    full_name: str
    email: EmailStr
    phone_number: str
    company_name: str

class ClientDeleteInput(BaseModel):
    client_id: int



def validate_create_client(**kwargs):
    try:
        user_input = ClientInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_client_view(e)


def validate_delete_client_input(**kwargs):
    try:
        user_input = ClientDeleteInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_client_view(e)


def validate_update_client(**kwargs):
    try:
        user_input = ClientInputUpdate(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_client_view(e)
