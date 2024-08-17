import pytest
from unittest.mock import patch, MagicMock
import datetime
import click

# Import the validation functions
from validators.click_validator import (
    validate_contract_id_is_signed,
    validate_email,
    validate_phone_number,
    validate_boolean,
    validate_client_by_sales,
    validate_amount,
    validate_date,
    validate_end_date,
    validate_attendees,
    validate_client,
    validate_event_id,
    validate_event_assigned_to_support_id,
    validate_collaborator,
    validate_commercial,
    validate_contract,
    validate_contract_by_collaborator,
    validate_role,
    validate_support,
    validate_employee_number,
)


def test_validate_email():
    # Test valid email
    assert validate_email(None, None, "test@example.com") == "test@example.com"

    # Test invalid email
    with pytest.raises(click.BadParameter):
        validate_email(None, None, "invalid-email")


def test_validate_phone_number():
    # Test valid phone number
    assert validate_phone_number(None, None, "+33123456789") == "+33123456789"
    assert validate_phone_number(None, None, "0123456789") == "0123456789"

    # Test invalid phone number
    with pytest.raises(click.BadParameter):
        validate_phone_number(None, None, "12345")


def test_validate_boolean():
    # Test various true values
    assert validate_boolean(None, None, "true") is True
    assert validate_boolean(None, None, "yes") is True
    assert validate_boolean(None, None, "1") is True

    # Test various false values
    assert validate_boolean(None, None, "false") is False
    assert validate_boolean(None, None, "no") is False
    assert validate_boolean(None, None, "0") is False

    # Test invalid boolean value
    with pytest.raises(click.BadParameter):
        validate_boolean(None, None, "maybe")


@patch("validators.click_validator.Client.get_by_id")
@patch("validators.click_validator.get_login_collaborator")
@patch("validators.click_validator.SessionLocal")
def test_validate_client_by_sales(
    mock_session, mock_get_login_collaborator, mock_get_by_id
):
    mock_session.return_value = MagicMock()
    mock_client = MagicMock()
    mock_client.commercial_collaborator_id = 1
    mock_get_by_id.return_value = mock_client
    mock_login_collaborator = MagicMock()
    mock_login_collaborator.id = 1
    mock_get_login_collaborator.return_value = mock_login_collaborator

    assert validate_client_by_sales(None, None, 1) == 1

    mock_login_collaborator.id = 2
    with pytest.raises(click.BadParameter):
        validate_client_by_sales(None, None, 1)


def test_validate_amount():
    ctx = MagicMock()
    ctx.params = {"total_amount": 100}

    assert validate_amount(ctx, None, 50) == 50

    with pytest.raises(click.BadParameter):
        validate_amount(ctx, None, 150)


def test_validate_date():
    ctx = MagicMock()

    valid_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
        "%Y-%m-%d %H:%M"
    )
    assert validate_date(ctx, None, valid_date) == valid_date

    past_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(
        "%Y-%m-%d %H:%M"
    )
    with pytest.raises(click.BadParameter):
        validate_date(ctx, None, past_date)

    with pytest.raises(click.BadParameter):
        validate_date(ctx, None, "invalid-date")


def test_validate_end_date():
    ctx = MagicMock()
    ctx.params = {
        "date_start": (
            datetime.datetime.now() + datetime.timedelta(days=1)
        ).strftime("%Y-%m-%d %H:%M")
    }

    valid_end_date = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime(
        "%Y-%m-%d %H:%M"
    )
    assert validate_end_date(ctx, None, valid_end_date) == valid_end_date

    invalid_end_date = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M")
    with pytest.raises(click.BadParameter):
        validate_end_date(ctx, None, invalid_end_date)


def test_validate_attendees():
    assert validate_attendees(None, None, 10) == 10

    with pytest.raises(click.BadParameter):
        validate_attendees(None, None, -5)

    with pytest.raises(click.BadParameter):
        validate_attendees(None, None, "invalid")


@patch("validators.click_validator.Client.get_by_id")
@patch("validators.click_validator.SessionLocal")
def test_validate_client(mock_session, mock_get_by_id):
    mock_session.return_value = MagicMock()
    mock_get_by_id.return_value = True  # Simulate a found client

    assert validate_client(None, None, 1) == 1

    mock_get_by_id.return_value = None  # Simulate a not found client
    with pytest.raises(click.BadParameter):
        validate_client(None, None, 1)


@patch("validators.click_validator.Event.get_by_id")
@patch("validators.click_validator.SessionLocal")
def test_validate_event_id(mock_session, mock_get_by_id):
    mock_session.return_value = MagicMock()
    mock_get_by_id.return_value = True  # Simulate a found event

    assert validate_event_id(None, None, 1) == 1

    mock_get_by_id.return_value = None  # Simulate a not found event
    with pytest.raises(click.BadParameter):
        validate_event_id(None, None, 1)


@patch("validators.click_validator.Event.get_by_id")
@patch("validators.click_validator.get_login_collaborator")
@patch("validators.click_validator.SessionLocal")
def test_validate_event_assigned_to_support_id(
    mock_session, mock_get_login_collaborator, mock_get_by_id
):
    mock_session.return_value = MagicMock()
    mock_event = MagicMock()
    mock_event.collaborator_support_id = 1
    mock_get_by_id.return_value = mock_event
    mock_login_collaborator = MagicMock()
    mock_login_collaborator.id = 1
    mock_get_login_collaborator.return_value = mock_login_collaborator

    assert validate_event_assigned_to_support_id(None, None, 1) == 1

    mock_login_collaborator.id = 2
    with pytest.raises(click.BadParameter):
        validate_event_assigned_to_support_id(None, None, 1)


@patch("validators.click_validator.Collaborator.get_by_id")
@patch("validators.click_validator.SessionLocal")
def test_validate_collaborator(mock_session, mock_get_by_id):
    mock_session.return_value = MagicMock()
    mock_get_by_id.return_value = True  # Simulate a found collaborator

    assert validate_collaborator(None, None, 1) == 1

    mock_get_by_id.return_value = None  # Simulate a not found collaborator
    with pytest.raises(click.BadParameter):
        validate_collaborator(None, None, 1)


@patch("validators.click_validator.Collaborator.get_by_id")
@patch("validators.click_validator.SessionLocal")
def test_validate_commercial(mock_session, mock_get_by_id):
    mock_session.return_value = MagicMock()
    mock_collaborator = MagicMock()
    mock_collaborator.role = "sales"
    mock_get_by_id.return_value = mock_collaborator

    assert validate_commercial(None, None, 1) == 1

    mock_collaborator.role = "support"  # Simulate a non-sales role
    with pytest.raises(click.BadParameter):
        validate_commercial(None, None, 1)


@patch("validators.click_validator.Contract.get_by_id")
@patch("validators.click_validator.SessionLocal")
def test_validate_contract(mock_session, mock_get_by_id):
    mock_session.return_value = MagicMock()
    mock_get_by_id.return_value = True  # Simulate a found contract

    assert validate_contract(None, None, 1) == 1

    mock_get_by_id.return_value = None  # Simulate a not found contract
    with pytest.raises(click.BadParameter):
        validate_contract(None, None, 1)


@patch("validators.click_validator.Contract.get_by_id")
@patch("validators.click_validator.SessionLocal")
def test_validate_contract_id_is_signed(mock_session, mock_get_by_id):
    mock_session.return_value = MagicMock()
    mock_contract = MagicMock()
    mock_contract.status = True
    mock_get_by_id.return_value = mock_contract

    assert validate_contract_id_is_signed(None, None, 1) == 1

    mock_contract.status = False  # Simulate an unsigned contract
    with pytest.raises(click.BadParameter):
        validate_contract_id_is_signed(None, None, 1)


@patch("validators.click_validator.Contract.get_by_id")
@patch("validators.click_validator.get_login_collaborator")
@patch("validators.click_validator.SessionLocal")
def test_validate_contract_by_collaborator(
    mock_session, mock_get_login_collaborator, mock_get_by_id
):
    mock_session.return_value = MagicMock()
    mock_contract = MagicMock()
    mock_contract.commercial_collaborator_id = 1
    mock_contract.status = True
    mock_get_by_id.return_value = mock_contract
    mock_login_collaborator = MagicMock()
    mock_login_collaborator.id = 1
    mock_login_collaborator.role = "sales"
    mock_get_login_collaborator.return_value = mock_login_collaborator

    assert validate_contract_by_collaborator(None, None, 1) == 1

    mock_login_collaborator.id = 2
    with pytest.raises(click.BadParameter):
        validate_contract_by_collaborator(None, None, 1)


@patch("validators.click_validator.Role.get_by_id")
@patch("validators.click_validator.SessionLocal")
def test_validate_role(mock_session, mock_get_by_id):
    mock_session.return_value = MagicMock()
    mock_get_by_id.return_value = True  # Simulate a found role

    assert validate_role(None, None, 1) == 1

    mock_get_by_id.return_value = None  # Simulate a not found role
    with pytest.raises(click.BadParameter):
        validate_role(None, None, 1)


@patch("validators.click_validator.Collaborator.get_by_id")
@patch("validators.click_validator.SessionLocal")
def test_validate_support(mock_session, mock_get_by_id):
    mock_session.return_value = MagicMock()
    mock_collaborator = MagicMock()
    mock_collaborator.role = "support"
    mock_get_by_id.return_value = mock_collaborator

    assert validate_support(None, None, 1) == 1

    mock_collaborator.role = "sales"  # Simulate a non-support role
    with pytest.raises(click.BadParameter):
        validate_support(None, None, 1)


@patch("validators.click_validator.Collaborator.get_by_employee_number")
@patch("validators.click_validator.SessionLocal")
def test_validate_employee_number(mock_session, mock_get_by_employee_number):
    mock_session.return_value = MagicMock()
    mock_get_by_employee_number.return_value = True  # Simulate a found employee

    assert validate_employee_number(None, None, 1) == 1

    mock_get_by_employee_number.return_value = None  # Simulate a not found employee
    with pytest.raises(click.BadParameter):
        validate_employee_number(None, None, 1)
