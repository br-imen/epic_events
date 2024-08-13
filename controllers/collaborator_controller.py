import os
from config.auth import create_access_token
from validators.collaborator_validator import (
    validate_collaborator_input,
    validate_delete_collaborator_input,
    validate_login_input,
)
from models.collaborator import Collaborator
from views.collaborator_view import (
    error_collaborator_non_found_view,
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
            success_create_collaborator_view()
        finally:
            session.close()


def update_collaborator_controller(employee_number, name, email, role_id, password):
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
                success_update_collaborator_view()
            else:
                error_collaborator_non_found_view()

        finally:
            session.close()


def delete_collaborator_controller(employee_number):
    data = {"employee_number": employee_number}
    validated_data = validate_delete_collaborator_input(**data)
    if validated_data:
        session = SessionLocal()
        try:
            collaborator = Collaborator.get_by_employee_number(
                employee_number, session
            )
            if collaborator:
                collaborator.delete(session)
                success_delete_collaborator_view()
            else:
                error_collaborator_non_found_view()
        finally:
            session.close()


def list_collaborators_controller():
    session = SessionLocal()
    try:
        collaborators = Collaborator.get_all(session)
        return list_collaborators_view(collaborators)
    finally:
        session.close()


# Controller to check collaborator email and create token if True
def authentication(email, password):
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
                error_invalid_email_password_view()
                return None
        finally:
            session.close()


# Logout
def logout_controller():
    # Define the path to the token file
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "epic_events")
    token_path = os.path.join(config_dir, "access_token.txt")

    # Check if the file exists
    if os.path.exists(token_path):
        # Delete the token file
        os.remove(token_path)
    success_logout_view()
