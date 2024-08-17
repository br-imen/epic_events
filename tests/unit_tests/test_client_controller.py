from unittest.mock import MagicMock, patch
from controllers.client_controller import (
    create_client_controller,
    update_client_controller,
    delete_client_controller,
    list_clients_controller,
)


def test_create_client_controller(mock_session):
    with patch(
        "controllers.client_controller.SessionLocal", return_value=mock_session
    ), patch(
        "controllers.client_controller.get_login_collaborator",
        return_value=MagicMock(id=1),
    ), patch(
        "controllers.client_controller.validate_create_client",
        return_value=MagicMock(dict=lambda: {}),
    ), patch(
        "controllers.client_controller.Collaborator.get_by_id",
        return_value=MagicMock(id=1),
    ), patch(
        "controllers.client_controller.Client.save"
    ) as mock_client_save, patch(
        "controllers.client_controller.success_create_client_view"
    ) as mock_success_view:

        create_client_controller(
            "foo Doe", "foo@example.com", "1234567890", "ABC Company"
        )
        mock_client_save.assert_called_once()
        mock_success_view.assert_called_once()


def test_update_client_controller(mock_session):
    with patch(
        "controllers.client_controller.SessionLocal", return_value=mock_session
    ), patch(
        "controllers.client_controller.get_login_collaborator",
        return_value=MagicMock(id=1),
    ), patch(
        "controllers.client_controller.validate_update_client",
        return_value=MagicMock(dict=lambda: {}),
    ), patch(
        "controllers.client_controller.Collaborator.get_by_id",
        return_value=MagicMock(id=1),
    ), patch(
        "controllers.client_controller.Client.get_by_id",
        return_value=MagicMock(id=1),
    ) as mock_get_by_id, patch(
        "controllers.client_controller.success_update_client_view"
    ) as mock_success_view:

        update_client_controller(
            1,
            "Updated foo Doe",
            "updated@example.com",
            "9876543210",
            "XYZ Company",
            1,
        )
        mock_get_by_id.assert_called_once()
        mock_success_view.assert_called_once()


def test_delete_client_controller(mock_session):
    with patch(
        "controllers.client_controller.SessionLocal", return_value=mock_session
    ), patch(
        "controllers.client_controller.get_login_collaborator",
        return_value=MagicMock(id=1),
    ), patch(
        "controllers.client_controller.validate_delete_client_input",
        return_value=MagicMock(dict=lambda: {}),
    ), patch(
        "controllers.client_controller.Collaborator.get_by_id",
        return_value=MagicMock(id=1),
    ), patch(
        "controllers.client_controller.Client.get_by_id",
        return_value=MagicMock(id=1),
    ) as mock_get_by_id, patch(
        "controllers.client_controller.success_delete_client_view"
    ) as mock_success_view:

        delete_client_controller(1)
        mock_get_by_id.assert_called_once()
        mock_success_view.assert_called_once()


def test_list_clients_controller(mock_session):
    with patch(
        "controllers.client_controller.SessionLocal", return_value=mock_session
    ), patch(
        "controllers.client_controller.get_login_collaborator",
        return_value=MagicMock(id=1),
    ), patch(
        "controllers.client_controller.Client.get_all", return_value=[]
    ), patch(
        "controllers.client_controller.list_client_view"
    ) as mock_list_clients_view:

        list_clients_controller()
        mock_list_clients_view.assert_called_once()
