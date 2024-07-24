from datetime import date
from pydantic import BaseModel, EmailStr


class ClientInput(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    company_name: str
    commercial_collaborator_id : int


class ClientInputUpdate(BaseModel):
    id = int
    full_name: str
    email: EmailStr
    phone_number: str
    company_name: str
    commercial_collaborator_id : int


class ClientDeleteInput(BaseModel):
    client_id: int
