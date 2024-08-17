from unittest.mock import patch
from models import Client
from controllers.client_controller import (
    create_client_controller,
    update_client_controller,
    delete_client_controller,
    list_clients_controller,
)


def test_create_client_integration(
    mock_auth_token, test_db, client_data, collaborator
):
    # Mock the get_login_collaborator to return the collaborator fixture
    with patch(
        "controllers.client_controller.get_login_collaborator",
        return_value=collaborator,
    ), patch("controllers.client_controller.SessionLocal", return_value=test_db):
        create_client_controller(**client_data)
    client_in_db = (
        test_db.query(Client).filter(Client.email == client_data["email"]).first()
    )
    assert client_in_db is not None
    assert client_in_db.full_name == client_data["full_name"]


def test_update_client_integration(test_db, collaborator, client):
    client_id = client.id
    updated_data = {
        "id": client_id,
        "full_name": "Foo Updated",
        "email": client.email,
        "phone_number": client.phone_number,
        "company_name": client.company_name,
        "commercial_collaborator_id": collaborator.id,
    }
    with patch(
        "controllers.client_controller.get_login_collaborator",
        return_value=collaborator,
    ), patch("controllers.client_controller.SessionLocal", return_value=test_db):
        update_client_controller(**updated_data)
    updated_client = test_db.query(Client).get(client_id)

    assert updated_client.full_name == "Foo Updated"


def test_delete_client_integration(test_db, collaborator, client):
    with patch(
        "controllers.client_controller.SessionLocal", return_value=test_db
    ), patch(
        "controllers.client_controller.get_login_collaborator",
        return_value=collaborator,
    ):
        client_in_db = (
            test_db.query(Client)
            .filter(Client.email == "foofloo@example.com")
            .first()
        )
        delete_client_controller(client_in_db.id)
        deleted_client = test_db.query(Client).get(client_in_db.id)

        assert deleted_client is None


def test_list_clients_integration(test_db, collaborator, client, capsys):
    with patch(
        "controllers.client_controller.SessionLocal", return_value=test_db
    ), patch(
        "controllers.client_controller.get_login_collaborator",
        return_value=collaborator,
    ):
        # Call the controller function,which will call list_client_view
        list_clients_controller()

        # Capture the printed output
        captured = capsys.readouterr()

        # Assertions
        # Ensure something was printed
        assert len(captured.out) > 0
        # Check that each client is printed as expected
        expected_output = "Client id=1, name=Foo floo, Email= foofloo@example.com,"
        assert expected_output in str(captured.out)
