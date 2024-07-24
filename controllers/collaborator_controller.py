from pydantic import ValidationError
from config.auth import create_access_token, is_authenticated
from controllers.collaborator_validator import (
    LoginInput,
    CollaboratorInput,
    DeleteCollaboratorInput,
)
from models.collaborator import Collaborator
from views.collaborator_view import (
    error_collaborator_non_found_view,
    success_delete_collaborator_view,
    success_login_view,
    success_create_collaborator_view,
    error_invalid_email_password_view,
    success_update_collaborator_view,
    validation_error_view,
    list_collaborators_view,
)
from config.database import SessionLocal


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
            print(new_collaborator.role)
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
            collaborator = Collaborator.get_by_employee_number(employee_number, session)
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
                access_token = create_access_token(data={"sub": collaborator.email, "role_id": collaborator.role_id})
                success_login_view()
                return {"access_token": access_token, "token_type": "bearer"}
            else:
                error_invalid_email_password_view()
                return None
        finally:
            session.close()
