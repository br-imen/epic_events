from unittest.mock import MagicMock, patch
from controllers.collaborator_controller import (
    create_collaborator_controller,
    update_collaborator_controller,
    delete_collaborator_controller,
    list_collaborators_controller,
)


def test_create_collaborator_controller(mock_session):
    with patch(
        "controllers.collaborator_controller.SessionLocal",
        return_value=mock_session,
    ), patch(
        "controllers.collaborator_controller.validate_collaborator_input",
        return_value=MagicMock(dict=lambda: {}),
    ), patch(
        "controllers.collaborator_controller.Collaborator.save"
    ) as mock_save, patch(
        "controllers.collaborator_controller.success_create_collaborator_view"
    ) as mock_success_view:

        create_collaborator_controller(
            "123", "foo Doe", "foo.doe@example.com", 1, "password"
        )
        mock_save.assert_called_once_with(mock_session)
        mock_success_view.assert_called_once()


def test_update_collaborator_controller(mock_session):
    with patch(
        "controllers.collaborator_controller.SessionLocal",
        return_value=mock_session,
    ), patch(
        "controllers.collaborator_controller.validate_collaborator_input",
        return_value=MagicMock(dict=lambda: {}),
    ), patch(
        "controllers.collaborator_controller.Collaborator.get_by_employee_number",
        return_value=MagicMock(employee_number="123"),
    ) as mock_get_by_employee_number, patch(
        "controllers.collaborator_controller.success_update_collaborator_view"
    ) as mock_success_view, patch(
        "controllers.collaborator_controller.error_collaborator_non_found_view"
    ) as mock_error_view:

        update_collaborator_controller(
            "123", "foo Doe", "foo.doe@example.com", 1, "password"
        )
        mock_get_by_employee_number.assert_called_once_with(
            employee_number="123", session=mock_session
        )
        mock_success_view.assert_called_once()
        mock_error_view.assert_not_called()


def test_delete_collaborator_controller(mock_session):
    with patch(
        "controllers.collaborator_controller.SessionLocal",
        return_value=mock_session,
    ), patch(
        "controllers.collaborator_controller.Collaborator.get_by_employee_number",
        return_value=MagicMock(employee_number="123"),
    ) as mock_get_by_employee_number, patch(
        "controllers.collaborator_controller.success_delete_collaborator_view"
    ) as mock_success_view, patch(
        "controllers.collaborator_controller.error_collaborator_non_found_view"
    ) as mock_error_view:

        delete_collaborator_controller("123")
        mock_get_by_employee_number.assert_called_once_with("123", mock_session)
        mock_success_view.assert_called_once()
        mock_error_view.assert_not_called()


def test_list_collaborators_controller(mock_session):
    with patch(
        "controllers.collaborator_controller.SessionLocal",
        return_value=mock_session,
    ), patch(
        "controllers.collaborator_controller.Collaborator.get_all",
        return_value=[
            MagicMock(employee_number="123"),
            MagicMock(employee_number="456"),
        ],
    ) as mock_get_all, patch(
        "controllers.collaborator_controller.list_collaborators_view"
    ) as mock_list_view:

        list_collaborators_controller()
        mock_get_all.assert_called_once_with(mock_session)
        mock_list_view.assert_called_once()
