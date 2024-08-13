from unittest.mock import patch
from pydantic import ValidationError
from decimal import Decimal

# Assuming the validators are in a module named 'validators'
from validators.contract_validator import (
    validate_create_contract_input,
    validate_delete_contract_input,
    validate_update_contract_input,
)

# Mock input data for the tests
valid_create_contract_data = {
    "client_id": 1,
    "commercial_collaborator_id": 2,
    "total_amount": Decimal("1000.00"),
    "amount_due": Decimal("500.00"),
    "status": True,
}

invalid_create_contract_data = {
    "client_id": 1,
    "commercial_collaborator_id": 2,
    "total_amount": Decimal("1000.00"),
    "amount_due": "invalid-decimal",  # Invalid decimal value
    "status": True,
}

valid_delete_contract_data = {"id": 1}

invalid_delete_contract_data = {"id": "invalid-id"}  # ID should be an integer

valid_update_contract_data = {
    "id": 1,
    "client_id": 1,
    "commercial_collaborator_id": 2,
    "total_amount": Decimal("1500.00"),
    "amount_due": Decimal("750.00"),
    "status": False,
}

invalid_update_contract_data = {
    "id": 1,
    "client_id": 1,
    "commercial_collaborator_id": 2,
    "total_amount": Decimal("1500.00"),
    "amount_due": "invalid-decimal",  # Invalid decimal value
    "status": False,
}


@patch("validators.contract_validator.validation_error_contract_view")
def test_validate_create_contract_input_valid(mock_validation_error):
    # Test with valid data
    user_input = validate_create_contract_input(**valid_create_contract_data)
    assert user_input.client_id == valid_create_contract_data["client_id"]
    assert (
        user_input.commercial_collaborator_id
        == valid_create_contract_data["commercial_collaborator_id"]
    )
    assert user_input.total_amount == valid_create_contract_data["total_amount"]
    assert user_input.amount_due == valid_create_contract_data["amount_due"]
    assert user_input.status == valid_create_contract_data["status"]
    mock_validation_error.assert_not_called()


@patch("validators.contract_validator.validation_error_contract_view")
def test_validate_create_contract_input_invalid(mock_validation_error):
    # Test with invalid data
    validate_create_contract_input(**invalid_create_contract_data)
    mock_validation_error.assert_called_once()
    assert isinstance(mock_validation_error.call_args[0][0], ValidationError)


@patch("validators.contract_validator.validation_error_contract_view")
def test_validate_delete_contract_input_valid(mock_validation_error):
    # Test with valid data
    user_input = validate_delete_contract_input(**valid_delete_contract_data)
    assert user_input.id == valid_delete_contract_data["id"]
    mock_validation_error.assert_not_called()


@patch("validators.contract_validator.validation_error_contract_view")
def test_validate_delete_contract_input_invalid(mock_validation_error):
    # Test with invalid data
    validate_delete_contract_input(**invalid_delete_contract_data)
    mock_validation_error.assert_called_once()
    assert isinstance(mock_validation_error.call_args[0][0], ValidationError)


@patch("validators.contract_validator.validation_error_contract_view")
def test_validate_update_contract_input_valid(mock_validation_error):
    # Test with valid data
    user_input = validate_update_contract_input(**valid_update_contract_data)
    assert user_input.id == valid_update_contract_data["id"]
    assert user_input.client_id == valid_update_contract_data["client_id"]
    assert (
        user_input.commercial_collaborator_id
        == valid_update_contract_data["commercial_collaborator_id"]
    )
    assert user_input.total_amount == valid_update_contract_data["total_amount"]
    assert user_input.amount_due == valid_update_contract_data["amount_due"]
    assert user_input.status == valid_update_contract_data["status"]
    mock_validation_error.assert_not_called()


@patch("validators.contract_validator.validation_error_contract_view")
def test_validate_update_contract_input_invalid(mock_validation_error):
    # Test with invalid data
    validate_update_contract_input(**invalid_update_contract_data)
    mock_validation_error.assert_called_once()
    assert isinstance(mock_validation_error.call_args[0][0], ValidationError)
