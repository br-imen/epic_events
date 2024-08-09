import pytest
from unittest.mock import MagicMock, patch
from models.event import Event
from controllers.event_controller import (
    create_event_controller,
    update_event_controller,
    delete_event_controller,
    list_events_controller,
)

def test_create_event_controller(mock_session):
    with patch("controllers.event_controller.SessionLocal", return_value=mock_session), \
        patch("controllers.event_controller.validate_create_event", return_value=MagicMock(dict=lambda: {})), \
        patch("controllers.event_controller.Event.save") as mock_event_save, \
        patch("controllers.event_controller.success_create_event_view") as mock_success_view:

        create_event_controller("123", "Event Title", "Event Description", "2022-01-01", "New York", [], "", "notes")
        mock_event_save.assert_called_once()
        mock_success_view.assert_called_once()

def test_update_event_controller(mock_session):
    with patch("controllers.event_controller.SessionLocal", return_value=mock_session), \
        patch("controllers.event_controller.validate_update_event", return_value=MagicMock(dict=lambda: {})), \
        patch("controllers.event_controller.Event.get_by_id", return_value=MagicMock(id=1)) as mock_get_by_id, \
        patch("controllers.event_controller.success_update_event_view") as mock_success_view, \
        patch("controllers.event_controller.error_event_not_found_view") as mock_error_view:

        update_event_controller(1, "Updated Event Title", "Updated Event Description", "2022-01-02", "Los Angeles")
        mock_get_by_id.assert_called_once()
        mock_success_view.assert_called_once()
        mock_error_view.assert_not_called()

def test_delete_event_controller(mock_session):
    with patch("controllers.event_controller.SessionLocal", return_value=mock_session), \
        patch("controllers.event_controller.validate_delete_event_input", return_value=MagicMock(dict=lambda: {})), \
        patch("controllers.event_controller.Event.get_by_id", return_value=MagicMock(id=1)) as mock_get_by_id, \
        patch("controllers.event_controller.success_delete_event_view") as mock_success_view, \
        patch("controllers.event_controller.error_event_not_found_view") as mock_error_view:

        delete_event_controller(1)
        mock_get_by_id.assert_called_once()
        mock_success_view.assert_called_once()
        mock_error_view.assert_not_called()

def test_list_events_controller(mock_session):
    with patch("controllers.event_controller.SessionLocal", return_value=mock_session), \
        patch("controllers.event_controller.Event.get_all", return_value=[]), \
        patch("controllers.event_controller.get_login_collaborator", return_value="mock_collaborator") as mock_get_login_collaborator, \
        patch("controllers.event_controller.list_event_view") as mock_list_events_view:

        list_events_controller(filters=[])
        mock_get_login_collaborator.assert_called_once_with(mock_session)
        mock_list_events_view.assert_called_once()