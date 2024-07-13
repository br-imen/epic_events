from functools import wraps
from config.auth import get_email_from_access_token, get_token_from_file
from models.collaborator import Collaborator


# Verify permission decorator
def has_permission(*permissions: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = get_token_from_file()
            email = get_email_from_access_token(token)
            collaborator = Collaborator.get_by_email(email)
            if not collaborator or not isinstance(collaborator, Collaborator):
                raise ValueError("Collaborator instance required")

            # Gather all the permission names of the collaborator's role
            collaborator_permissions = {
                permission.name for permission in collaborator.role.permissions
            }

            # Check if all required permissions are in the collaborator's permissions
            if not all(
                permission in collaborator_permissions for permission in permissions
            ):
                raise PermissionError(
                    f"Collaborator does not have all the required permissions: {permissions}"
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator
