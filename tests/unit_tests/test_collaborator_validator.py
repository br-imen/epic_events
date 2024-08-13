from unittest.mock import patch
from pydantic import ValidationError

# Assuming the validators are in a module named 'validators'
from validators.collaborator_validator import (
    validate_login_input,
    validate_collaborator_input,
)

# Mock input data for the tests
valid_login_data = {
    "email": "foodoe@example.com",
    "password": "securepassword123",
}

invalid_login_data = {
    "email": "foodoe@example",
    "password": "",  # Password is required but empty
}

valid_collaborator_data = {
    "email": "foodoe@example.com",
    "password": "securepassword123",
    "employee_number": 12345,
    "name": "foo Doe",
    "role_id": 1,
}

invalid_collaborator_data = {
    "email": "foodoe@example.com",
    "password": "123",  # Password is too short
    "employee_number": 12345,
    "name": "foo Doe",
    "role_id": 1,
}

valid_delete_collaborator_data = {"employee_number": 12345}

invalid_delete_collaborator_data = {
    "employee_number": "not-a-number"  # Employee number should be an integer
}


@patch("validators.collaborator_validator.validation_error_view")
def test_validate_login_input_valid(mock_validation_error_view):
    # Test with valid data
    user_input = validate_login_input(**valid_login_data)
    assert user_input.email == valid_login_data["email"]
    assert user_input.password == valid_login_data["password"]
    mock_validation_error_view.assert_not_called()


@patch("validators.collaborator_validator.validation_error_view")
def test_validate_login_input_invalid(mock_validation_error_view):
    # Test with invalid data
    validate_login_input(**invalid_login_data)
    mock_validation_error_view.assert_called_once()
    assert isinstance(mock_validation_error_view.call_args[0][0], ValidationError)


@patch("validators.collaborator_validator.validation_error_view")
def test_validate_collaborator_input_valid(mock_validation_error_view):
    # Test with valid data
    user_input = validate_collaborator_input(**valid_collaborator_data)
    assert user_input.email == valid_collaborator_data["email"]
    assert user_input.password == valid_collaborator_data["password"]
    assert user_input.employee_number == valid_collaborator_data["employee_number"]
    assert user_input.name == valid_collaborator_data["name"]
    assert user_input.role_id == valid_collaborator_data["role_id"]
    mock_validation_error_view.assert_not_called()


@patch("validators.collaborator_validator.validation_error_view")
def test_validate_collaborator_input_invalid(mock_validation_error_view):
    # Test with invalid data
    validate_collaborator_input(**invalid_collaborator_data)
    mock_validation_error_view.assert_called_once()
