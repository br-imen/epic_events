from config.auth import get_login_collaborator
from models import Client, Collaborator
from config.database import SessionLocal
from validators.client_validator import (
    validate_create_client,
    validate_delete_client_input,
    validate_update_client,
)
from views.base_view import permission_denied_view
from views.client_view import (
    error_client_not_found_view,
    error_commercial_not_found_view,
    list_client_view,
    success_create_client_view,
    success_delete_client_view,
    success_update_client_view,
)

def create_client_controller(
    full_name, email, phone_number, company_name
):
    session = SessionLocal()
    collaborator = get_login_collaborator(session=session)
    commercial_collaborator_id = collaborator.id
    client_data = {
        "full_name": full_name,
        "email": email,
        "phone_number": phone_number,
        "company_name": company_name,
        "commercial_collaborator_id": commercial_collaborator_id,
    }
    validated_data = validate_create_client(**client_data)
    if validated_data:
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
    id, full_name, email, phone_number, company_name
):
    session = SessionLocal()
    login_collaborator = get_login_collaborator(session=session)
    login_collaborator_id = login_collaborator.id
    client_data = {
        "id": id,
        "full_name": full_name,
        "email": email,
        "phone_number": phone_number,
        "company_name": company_name,
    }
    validated_data = validate_update_client(**client_data)
    if validated_data:
        try:
            client = Client.get_by_id(id, session)
            if client:
                if login_collaborator_id != client.commercial_collaborator_id:
                    permission_denied_view()
                    exit(1)
                client.update(session, **validated_data.dict())
                success_update_client_view()
            else:
                error_client_not_found_view()
        finally:
            session.close()


def delete_client_controller(client_id):
    data = {"client_id": client_id}
    validated_data = validate_delete_client_input(**data)
    session = SessionLocal()
    login_collaborator = get_login_collaborator(session=session)
    login_collaborator_id = login_collaborator.id
    if validated_data:
        try:
            session = SessionLocal()
            client = Client.get_by_id(client_id, session)
            if client:
                if login_collaborator_id != client.commercial_collaborator_id:
                    permission_denied_view()
                    exit(1)
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
