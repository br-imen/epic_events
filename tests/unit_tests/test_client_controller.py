import pytest
from unittest.mock import patch
from models.client import Client
from controllers.client_controller import (
    create_client_controller,
    update_client_controller,
    delete_client_controller,
    list_clients_controller,
)

def test_create_client_controller(session, collaborator, mock_login_collaborator, mock_session_local):
    with patch("controllers.client_controller.get_login_collaborator", return_value=collaborator):
        create_client_controller("John Doe", "john@example.com", "123456789", "Acme Corp")
    client = session.query(Client).filter_by(email="john@example.com").first()
    assert client is not None
    assert client.full_name == "John Doe"
    assert client.phone_number == "123456789"
    assert client.company_name == "Acme Corp"
    assert client.commercial_collaborator_id == collaborator.id

def test_update_client_controller(session, collaborator, mock_login_collaborator, mock_session_local):
    # First create a client
    with patch("controllers.client_controller.get_login_collaborator", return_value=collaborator):
        create_client_controller("John Doe", "john@example.com", "123456789", "Acme Corp")
    client = session.query(Client).filter_by(email="john@example.com").first()
    
    # Now update the client
    with patch("controllers.client_controller.get_login_collaborator", return_value=collaborator):
        update_client_controller(client.id, "John Smith", "johnsmith@example.com", "987654321", "Smith Corp")
    updated_client = session.query(Client).filter_by(id=client.id).first()
    
    assert updated_client is not None
    assert updated_client.full_name == "John Smith"
    assert updated_client.email == "johnsmith@example.com"
    assert updated_client.phone_number == "987654321"
    assert updated_client.company_name == "Smith Corp"

def test_delete_client_controller(session, collaborator, mock_login_collaborator, mock_session_local):
    # First create a client
    with patch("controllers.client_controller.get_login_collaborator", return_value=collaborator):
        create_client_controller("John Doe", "john@example.com", "123456789", "Acme Corp")
    client = session.query(Client).filter_by(email="john@example.com").first()
    
    # Now delete the client
    with patch("controllers.client_controller.get_login_collaborator", return_value=collaborator):
        delete_client_controller(client.id)
    deleted_client = session.query(Client).filter_by(id=client.id).first()
    
    assert deleted_client is None

def test_list_clients_controller(session, collaborator, mock_login_collaborator, mock_session_local):
    # Create a couple of clients
    with patch("controllers.client_controller.get_login_collaborator", return_value=collaborator):
        create_client_controller("John Doe", "john@example.com", "123456789", "Acme Corp")
        create_client_controller("Jane Smith", "jane@example.com", "987654321", "Smith Inc")
    
    # List clients
    clients = list_clients_controller()
    
    assert len(clients) == 2
    assert clients[0].email in ["john@example.com", "jane@example.com"]
    assert clients[1].email in ["john@example.com", "jane@example.com"]
