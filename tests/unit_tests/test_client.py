import pytest
import datetime
from unittest.mock import MagicMock
from models.client import Client

def test_save(mock_session, client):
    client.save(mock_session)
    mock_session.add.assert_called_once_with(client)
    mock_session.commit.assert_called_once()

def test_update(mock_session, client):
    client.update(mock_session, full_name="fool Doe")
    assert client.full_name == "fool Doe"
    assert client.last_contact is not None
    mock_session.merge.assert_called_once_with(client)
    mock_session.commit.assert_called_once()

def test_delete(mock_session, client):
    client.delete(mock_session)
    mock_session.delete.assert_called_once_with(client)
    mock_session.commit.assert_called_once()

def test_get_by_id(mock_session):
    client_id = 1
    mock_client = MagicMock(id=client_id)
    mock_session.query.return_value.filter.return_value.first.return_value = mock_client
    client = Client.get_by_id(client_id, mock_session)
    assert client.id == client_id
    mock_session.query.assert_called_once_with(Client)
    mock_session.query.return_value.filter.return_value.first.assert_called_once()

def test_get_all(mock_session):
    mock_clients = [MagicMock(id=1), MagicMock(id=2)]
    mock_session.query.return_value.all.return_value = mock_clients
    clients = Client.get_all(mock_session)
    assert len(clients) == 2
    mock_session.query.assert_called_once_with(Client)
    mock_session.query.return_value.all.assert_called_once()

def test_str():
    client = Client(
        id=1,
        full_name="foo Doe",
        email="foo@example.com",
        phone_number="1234567890",
        company_name="ABC Corp",
        creation_date=datetime.datetime(2022, 1, 1),
        last_contact=datetime.datetime(2022, 1, 2),
        commercial_collaborator_id=2
    )
    expected_output = (
        "Client 1: foo Doe, Email: foo@example.com, Phone: 1234567890, "
        "Company: ABC Corp, Created: 2022-01-01 00:00:00, Last Contact: 2022-01-02 00:00:00, Commercial id: 2"
    )
    assert str(client) == expected_output