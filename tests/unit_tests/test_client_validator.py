import pytest
from pydantic import ValidationError
from unittest.mock import patch

# Assuming the validators are in a module named 'validators'
from validators.client_validator import validate_create_client, validate_delete_client_input, validate_update_client

# Mock input data for the tests
valid_create_client_data = {
    "full_name": "foo Doe",
    "email": "foodoe@example.com",
    "phone_number": "+33123456789",
    "company_name": "Example Corp",
    "commercial_collaborator_id": "12345"
}

invalid_create_client_data = {
    "full_name": "foo Doe",
    "email": "invalid-email",
    "phone_number": "+33123456789",
    "company_name": "Example Corp",
    "commercial_collaborator_id": "12345"
}

valid_delete_client_data = {
    "client_id": 1
}

invalid_delete_client_data = {
    "client_id": "invalid-id"
}

valid_update_client_data = {
    "id": 1,
    "full_name": "name Updated",
    "email": "namesurnameupdated@example.com",
    "phone_number": "+33123456789",
    "company_name": "Updated Corp"
}

invalid_update_client_data = {
    "id": "invalid-id",
    "full_name": "name surname Updated",
    "email": "namesurnameupdated@example.com",
    "phone_number": "+33123456789",
    "company_name": "Updated Corp"
}


@patch('validators.client_validator.validation_error_client_view')
def test_validate_create_client_valid(mock_validation_error):
    # Test with valid data
    user_input = validate_create_client(**valid_create_client_data)
    assert user_input.full_name == valid_create_client_data["full_name"]
    assert user_input.email == valid_create_client_data["email"]
    assert user_input.phone_number == valid_create_client_data["phone_number"]
    assert user_input.company_name == valid_create_client_data["company_name"]
    assert user_input.commercial_collaborator_id == valid_create_client_data["commercial_collaborator_id"]
    mock_validation_error.assert_not_called()

@patch('validators.client_validator.validation_error_client_view')
def test_validate_create_client_invalid(mock_validation_error):
    # Test with invalid data
    validate_create_client(**invalid_create_client_data)
    mock_validation_error.assert_called_once()
    assert isinstance(mock_validation_error.call_args[0][0], ValidationError)


@patch('validators.client_validator.validation_error_client_view')
def test_validate_delete_client_input_valid(mock_validation_error):
    # Test with valid data
    user_input = validate_delete_client_input(**valid_delete_client_data)
    assert user_input.client_id == valid_delete_client_data["client_id"]
    mock_validation_error.assert_not_called()

@patch('validators.client_validator.validation_error_client_view')
def test_validate_delete_client_input_invalid(mock_validation_error):
    # Test with invalid data
    validate_delete_client_input(**invalid_delete_client_data)
    mock_validation_error.assert_called_once()
    assert isinstance(mock_validation_error.call_args[0][0], ValidationError)


@patch('validators.client_validator.validation_error_client_view')
def test_validate_update_client_valid(mock_validation_error):
    # Test with valid data
    user_input = validate_update_client(**valid_update_client_data)
    assert user_input.id == valid_update_client_data["id"]
    assert user_input.full_name == valid_update_client_data["full_name"]
    assert user_input.email == valid_update_client_data["email"]
    assert user_input.phone_number == valid_update_client_data["phone_number"]
    assert user_input.company_name == valid_update_client_data["company_name"]
    mock_validation_error.assert_not_called()

@patch('validators.client_validator.validation_error_client_view')
def test_validate_update_client_invalid(mock_validation_error):
    # Test with invalid data
    validate_update_client(**invalid_update_client_data)
    mock_validation_error.assert_called_once()
    assert isinstance(mock_validation_error.call_args[0][0], ValidationError)
