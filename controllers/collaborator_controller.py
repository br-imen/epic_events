import os
from config.auth import create_access_token, get_login_collaborator
from validators.collaborator_validator import (
    validate_collaborator_input,
    validate_delete_collaborator_input,
    validate_login_input,
)
from models.collaborator import Collaborator
from views.collaborator_view import (
    display_user_infos,
    error_collaborator_not_found_view,
    success_delete_collaborator_view,
    success_login_view,
    success_create_collaborator_view,
    error_invalid_email_password_view,
    success_logout_view,
    success_update_collaborator_view,
    list_collaborators_view,
)
from config.database import SessionLocal


def create_collaborator_controller(employee_number, name, email, role_id, password):
    """
    Create a new collaborator.

    Args:
        employee_number (int): The employee number of the collaborator.
        name (str): The name of the collaborator.
        email (str): The email address of the collaborator.
        role_id (int): The role ID of the collaborator.
        password (str): The password of the collaborator.

    Returns:
        None
    """
    collaborator_data = {
        "employee_number": employee_number,
        "name": name,
        "email": email,
        "role_id": role_id,
        "password": password,
    }
    validated_data = validate_collaborator_input(**collaborator_data)
    if validated_data:
        session = SessionLocal()
        try:
            new_collaborator = Collaborator(**validated_data.dict())
            new_collaborator.save(session)
            success_create_collaborator_view(new_collaborator)
        finally:
            session.close()


def update_collaborator_controller(employee_number, name, email, role_id, password):
    """
    Update a collaborator with the given employee number.

    Args:
        employee_number (int): The employee number of the collaborator.
        name (str): The name of the collaborator.
        email (str): The email of the collaborator.
        role_id (int): The role ID of the collaborator.
        password (str): The password of the collaborator.

    Returns:
        None
    """
    collaborator_data = {
        "employee_number": employee_number,
        "name": name,
        "email": email,
        "role_id": role_id,
        "password": password,
    }
    validated_data = validate_collaborator_input(**collaborator_data)
    if validated_data:
        session = SessionLocal()
        try:
            collaborator = Collaborator.get_by_employee_number(
                employee_number=employee_number, session=session
            )
            if collaborator:
                collaborator.update(session, **validated_data.dict())
                success_update_collaborator_view(collaborator)
            else:
                error_collaborator_not_found_view(employee_number=employee_number)

        finally:
            session.close()


def delete_collaborator_controller(employee_number):
    """
    Deletes a collaborator with the given employee number.

    Args:
        employee_number (int): The employee number of the collaborator to be deleted.

    Returns:
        None
    """
    data = {"employee_number": employee_number}
    validated_data = validate_delete_collaborator_input(**data)
    if validated_data:
        session = SessionLocal()
        try:
            collaborator = Collaborator.get_by_employee_number(
                employee_number, session
            )
            if collaborator:
                collaborator_infos = collaborator.__dict__
                collaborator.delete(session)
                success_delete_collaborator_view(collaborator_infos)
            else:
                error_collaborator_not_found_view(employee_number=employee_number)
        finally:
            session.close()


def list_collaborators_controller():
    """
    Retrieves a list of collaborators from the database and returns the view
    for displaying the list.

    Returns:
        list: The view for displaying the list of collaborators.
    """
    session = SessionLocal()
    try:
        collaborators = Collaborator.get_all(session)
        return list_collaborators_view(collaborators)
    finally:
        session.close()


# Controller to check collaborator email and create token if True
def authentication(email, password):
    """
    Authenticates a collaborator using the provided email and password.

    Args:
        email (str): The email of the collaborator.
        password (str): The password of the collaborator.

    Returns:
        dict or None: A dictionary containing the access token and token type
        if the authentication is successful,
        None otherwise.
    """

    login_data = {"email": email, "password": password}
    validated_login_data = validate_login_input(**login_data)
    if validated_login_data:
        session = SessionLocal()
        try:
            collaborator = Collaborator.get_by_email(email, session)
            if collaborator and collaborator.verify_password(password):
                access_token = create_access_token(
                    data={
                        "sub": collaborator.email,
                        "role_id": collaborator.role_id,
                    }
                )
                success_login_view()
                return {"access_token": access_token, "token_type": "bearer"}
            else:
                error_invalid_email_password_view(email)
                return None
        finally:
            session.close()


# Logout
def logout_controller():
    """
    Logs out the user by deleting the access token file.
    """
    home_directory = os.path.expanduser("~")
    token_path = os.path.join(home_directory, os.getenv("TOKEN_DIR_PATH"),
                              os.getenv("TOKEN_FILENAME"))
    # Check if the file exists
    if os.path.exists(token_path):
        # Delete the token file
        os.remove(token_path)
    success_logout_view()


def whoami_controller():
    """
    Retrieves the name of the currently logged in collaborator.
    """
    try:
        session = SessionLocal()
        user = get_login_collaborator(session)
        display_user_infos(user)
    except FileNotFoundError:
        return None
    finally:
        session.close()
