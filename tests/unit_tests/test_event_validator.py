import pytest
from unittest.mock import patch
from pydantic import ValidationError
from datetime import datetime, timedelta

# Assuming the validators are in a module named 'validators'
from validators.event_validator import (
    validate_create_event,
    validate_delete_event_input,
    validate_update_event,
)

# Mock input data for the tests
valid_create_event_data = {
    "client_id": 1,
    "contract_id": 1,
    "description": "Event Description",
    "date_start": datetime.now() + timedelta(days=1),
    "date_end": datetime.now() + timedelta(days=2),
    "collaborator_support_id": 2,
    "location": "Event Location",
    "attendees": 100,
    "notes": "Some notes"
}

invalid_create_event_data_end_date = {
    "client_id": 1,
    "contract_id": 1,
    "description": "Event Description",
    "date_start": datetime.now() + timedelta(days=2),
    "date_end": datetime.now() + timedelta(days=1),  # End date before start date
    "collaborator_support_id": 2,
    "location": "Event Location",
    "attendees": 100,
    "notes": "Some notes"
}

invalid_create_event_data_attendees = {
    "client_id": 1,
    "contract_id": 1,
    "description": "Event Description",
    "date_start": datetime.now() + timedelta(days=1),
    "date_end": datetime.now() + timedelta(days=2),
    "collaborator_support_id": 2,
    "location": "Event Location",
    "attendees": -10,  # Negative number of attendees
    "notes": "Some notes"
}

valid_update_event_data = {
    "id": 1,
    "client_id": 1,
    "contract_id": 1,
    "description": "Updated Event Description",
    "date_start": datetime.now() + timedelta(days=3),
    "date_end": datetime.now() + timedelta(days=4),
    "collaborator_support_id": 2,
    "location": "Updated Event Location",
    "attendees": 150,
    "notes": "Updated notes"
}

invalid_update_event_data_end_date = {
    "id": 1,
    "client_id": 1,
    "contract_id": 1,
    "description": "Updated Event Description",
    "date_start": datetime.now() + timedelta(days=4),
    "date_end": datetime.now() + timedelta(days=3),  # End date before start date
    "collaborator_support_id": 2,
    "location": "Updated Event Location",
    "attendees": 150,
    "notes": "Updated notes"
}

invalid_update_event_data_attendees = {
    "id": 1,
    "client_id": 1,
    "contract_id": 1,
    "description": "Updated Event Description",
    "date_start": datetime.now() + timedelta(days=3),
    "date_end": datetime.now() + timedelta(days=4),
    "collaborator_support_id": 2,
    "location": "Updated Event Location",
    "attendees": -20,  # Negative number of attendees
    "notes": "Updated notes"
}

valid_delete_event_data = {
    "id": 1
}

invalid_delete_event_data = {
    "id": "invalid-id"  # ID should be an integer
}


@patch('validators.event_validator.validation_error_event_view')
def test_validate_create_event_valid(mock_validation_error):
    # Test with valid data
    user_input = validate_create_event(**valid_create_event_data)
    assert user_input.client_id == valid_create_event_data["client_id"]
    assert user_input.contract_id == valid_create_event_data["contract_id"]
    assert user_input.description == valid_create_event_data["description"]
    assert user_input.date_start == valid_create_event_data["date_start"]
    assert user_input.date_end == valid_create_event_data["date_end"]
    assert user_input.collaborator_support_id == valid_create_event_data["collaborator_support_id"]
    assert user_input.location == valid_create_event_data["location"]
    assert user_input.attendees == valid_create_event_data["attendees"]
    assert user_input.notes == valid_create_event_data["notes"]
    mock_validation_error.assert_not_called()

@patch('validators.event_validator.validation_error_event_view')
def test_validate_create_event_invalid_end_date(mock_validation_error):
    # Test with end date before start date
    validate_create_event(**invalid_create_event_data_end_date)
    mock_validation_error.assert_called_once()
    assert isinstance(mock_validation_error.call_args[0][0], ValidationError)

@patch('validators.event_validator.validation_error_event_view')
def test_validate_create_event_invalid_attendees(mock_validation_error):
    # Test with negative attendees
    validate_create_event(**invalid_create_event_data_attendees)
    mock_validation_error.assert_called_once()
    assert isinstance(mock_validation_error.call_args[0][0], ValidationError)


@patch('validators.event_validator.validation_error_event_view')
def test_validate_update_event_valid(mock_validation_error):
    # Test with valid data
    user_input = validate_update_event(**valid_update_event_data)
    assert user_input.id == valid_update_event_data["id"]
    assert user_input.client_id == valid_update_event_data["client_id"]
    assert user_input.contract_id == valid_update_event_data["contract_id"]
    assert user_input.description == valid_update_event_data["description"]
    assert user_input.date_start == valid_update_event_data["date_start"]
    assert user_input.date_end == valid_update_event_data["date_end"]
    assert user_input.collaborator_support_id == valid_update_event_data["collaborator_support_id"]
    assert user_input.location == valid_update_event_data["location"]
    assert user_input.attendees == valid_update_event_data["attendees"]
    assert user_input.notes == valid_update_event_data["notes"]
    mock_validation_error.assert_not_called()

@patch('validators.event_validator.validation_error_event_view')
def test_validate_update_event_invalid_end_date(mock_validation_error):
    # Test with end date before start date
    validate_update_event(**invalid_update_event_data_end_date)
    mock_validation_error.assert_called_once()
    assert isinstance(mock_validation_error.call_args[0][0], ValidationError)

@patch('validators.event_validator.validation_error_event_view')
def test_validate_update_event_invalid_attendees(mock_validation_error):
    # Test with negative attendees
    validate_update_event(**invalid_update_event_data_attendees)
    mock_validation_error.assert_called_once()
    assert isinstance(mock_validation_error.call_args[0][0], ValidationError)


@patch('validators.event_validator.validation_error_event_view')
def test_validate_delete_event_input_valid(mock_validation_error):
    # Test with valid data
    user_input = validate_delete_event_input(**valid_delete_event_data)
    assert user_input.id == valid_delete_event_data["id"]
    mock_validation_error.assert_not_called()

@patch('validators.event_validator.validation_error_event_view')
def test_validate_delete_event_input_invalid(mock_validation_error):
    # Test with invalid data
    validate_delete_event_input(**invalid_delete_event_data)
    mock_validation_error.assert_called_once()
    assert isinstance(mock_validation_error.call_args[0][0], ValidationError)
