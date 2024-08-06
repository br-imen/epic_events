from functools import wraps
from config.auth import get_email_from_access_token, get_token_from_file
from models.collaborator import Collaborator
from models import Role
from sqlalchemy.orm import Session
from config.database import SessionLocal

def has_permission(*permissions: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = get_token_from_file()
            email = get_email_from_access_token(token)
            
            session: Session = SessionLocal()
            collaborator = session.query(Collaborator).filter_by(email=email).first()
            if not collaborator or not isinstance(collaborator, Collaborator):
                raise ValueError("Collaborator instance required")

            role = session.query(Role).filter_by(id=collaborator.role_id).first()
            if not role:
                raise ValueError("Role not found")

            collaborator_permissions = {permission.name for permission in role.permissions}

            if not all(permission in collaborator_permissions for permission in permissions):
                raise PermissionError(f"Collaborator does not have all the required permissions: {permissions}")

            return func(*args, **kwargs)

        return wrapper

    return decorator
