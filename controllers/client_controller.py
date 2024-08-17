from config.auth import get_login_collaborator
from models import Client, Collaborator
from config.database import SessionLocal
from validators.client_validator import (
    validate_create_client,
    validate_delete_client_input,
    validate_update_client,
)
from views.client_view import (
    error_commercial_not_found_view,
    list_client_view,
    success_create_client_view,
    success_delete_client_view,
    success_update_client_view,
)


def create_client_controller(full_name, email, phone_number, company_name):
    """
    Create a new client with the given information.

    Args:
        full_name (str): The full name of the client.
        email (str): The email address of the client.
        phone_number (str): The phone number of the client.
        company_name (str): The name of the client's company.

    Returns:
        None
    """
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
            found_commercial = Collaborator.get_by_id(
                commercial_collaborator_id, session
            )
            if found_commercial:
                new_client = Client(**validated_data.dict())
                new_client.save(session)
                success_create_client_view()
            else:
                error_commercial_not_found_view(commercial_collaborator_id)
        finally:
            session.close()


def update_client_controller(id, full_name, email, phone_number,
                             company_name, commercial_collaborator_id):
    """
    Update a client's information in the database.

    Args:
        id (int): The ID of the client.
        full_name (str): The full name of the client.
        email (str): The email address of the client.
        phone_number (str): The phone number of the client.
        company_name (str): The name of the client's company.
        commercial_collaborator_id (int): The ID of the collaborator responsible

    Returns:
        None
    """
    session = SessionLocal()
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
        try:
            client = Client.get_by_id(id, session)
            client.update(session, **validated_data.dict())
            success_update_client_view()
        finally:
            session.close()


def delete_client_controller(client_id):
    """
    Deletes a client from the database.

    Args:
        client_id (int): The ID of the client to be deleted.

    Returns:
        None
    """
    data = {"client_id": client_id}
    validated_data = validate_delete_client_input(**data)
    session = SessionLocal()
    if validated_data:
        try:
            session = SessionLocal()
            client = Client.get_by_id(client_id, session)
            client.delete(session)
            success_delete_client_view()
        finally:
            session.close()


def list_clients_controller():
    """
    Retrieves a list of clients from the database and returns the view for
    displaying the list.

    Returns:
        list: The view for displaying the list of clients.
    """
    session = SessionLocal()
    try:
        clients = Client.get_all(session)
        return list_client_view(clients)
    finally:
        session.close()
