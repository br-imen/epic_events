from pydantic import ValidationError
from models import Client, Collaborator
from config.database import SessionLocal
from controllers.client_validator import (
    ClientDeleteInput,
    ClientInput,
    ClientInputUpdate,
)
from views.client_view import (
    error_client_not_found_view,
    error_commercial_not_found_view,
    list_client_view,
    success_create_client_view,
    success_delete_client_view,
    success_update_client_view,
    validation_error_client_view,
)


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


def create_client_controller(
    full_name, email, phone_number, company_name, commercial_collaborator_id
):
    client_data = {
        "full_name": full_name,
        "email": email,
        "phone_number": phone_number,
        "company_name": company_name,
        "commercial_collaborator_id": commercial_collaborator_id,
    }
    validated_data = validate_create_client(**client_data)
    if validated_data:
        session = SessionLocal()
        try:
            found_commercial = Collaborator.get_by_id(commercial_collaborator_id, session)
            if found_commercial:
                new_client = Client(**validated_data.dict())
                new_client.save(session)
                success_create_client_view()
            else:
                error_commercial_not_found_view()
        finally:
            session.close()


def update_client_controller(
    id, full_name, email, phone_number, company_name, commercial_collaborator_id
):
    client_data = {
        "id": id,
        "full_name": full_name,
        "email": email,
        "phone_number": phone_number,
        "company_name": company_name,
        "commercial_collaborator_id": commercial_collaborator_id,
    }
    validated_data = validate_update_client(**client_data)
    if validated_data:
        session = SessionLocal()
        try:
            client = Client.get_by_id(id, session)
            if client:
                collaborator = Collaborator.get_by_id(
                    commercial_collaborator_id, session=session
                )
                if collaborator:
                    client.update(session, **validated_data.dict())
                    success_update_client_view()
                else:
                    error_commercial_not_found_view()
            else:
                error_client_not_found_view()
        finally:
            session.close()


def delete_client_controller(client_id):
    data = {"client_id": client_id}
    validated_data = validate_delete_client_input(**data)
    if validated_data:
        try:
            session = SessionLocal()
            client = Client.get_by_id(client_id, session)
            if client:
                client.delete(session)
                success_delete_client_view()
            else:
                error_client_not_found_view()
        finally:
            session.close()


def list_clients_controller():
    session = SessionLocal()
    try:
        clients = Client.get_all(session)
        return list_client_view(clients)
    finally:
        session.close()
