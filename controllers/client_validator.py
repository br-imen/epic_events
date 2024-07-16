from datetime import date
from pydantic import BaseModel, EmailStr


class ClientInput(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    company_name: str
    contact_commercial: str


class ClientInputUpdate(BaseModel):
    id = int
    full_name: str
    email: EmailStr
    phone_number: str
    company_name: str
    contact_commercial: str


class ClientDeleteInput(BaseModel):
    client_id: int
