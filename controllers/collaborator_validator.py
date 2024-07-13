from pydantic import BaseModel, EmailStr, constr


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
