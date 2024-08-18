from datetime import datetime
import re

import click

from config.auth import get_login_collaborator
from config.database import SessionLocal
from models.client import Client
from models.collaborator import Collaborator, Role
from models.contract import Contract
from models.event import Event


# Validates an email address format.
def validate_email(ctx, param, value):
    """
    Validates the format of an email address.

    Args:
        ctx (click.Context): The click context.
        param (click.Parameter): The click parameter.
        value (str): The value to be validated.

    Raises:
        click.BadParameter: If the email address format is invalid.

    Returns:
        str: The validated email address.
    """
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
        raise click.BadParameter("Invalid email address format")
    return value


def validate_email_exist(ctx, param, value):
    validate_email(ctx, param, value)
    session = SessionLocal()
    collaborator = Collaborator.get_by_email(value, session)
    employee_number = ctx.params.get("employee_number")
    collaborator_by_employee_number = Collaborator.get_by_employee_number(
        employee_number,
        session
    )
    if collaborator and collaborator != collaborator_by_employee_number:
        raise click.BadParameter("Email already exists")
    session.close()
    return value


# Validate_phone_number
def validate_phone_number(ctx, param, value):
    """
    Validates the format of a phone number.
    Args:
        ctx (click.Context): The click context.
        param (click.Parameter): The click parameter.
        value (str): The phone number to validate.
    Returns:
        str: The validated phone number.
    Raises:
        click.BadParameter: If the phone number has an invalid format.
    """
    if not re.match(r"^(\+33|0)\d{9}$", value):
        raise click.BadParameter("Invalid phone number format")
    return value


# Validate bool input status:
def validate_boolean(ctx, param, value):
    """
    Validates a boolean value.

    Args:
        ctx (click.Context): The click context.
        param (click.Parameter): The click parameter.
        value (Any): The value to be validated.

    Returns:
        bool: The validated boolean value.

    Raises:
        click.BadParameter: If the value is not a valid boolean.

    """
    if isinstance(value, str):
        value = value.lower()
        if value in ["true", "t", "yes", "y", "1"]:
            return True
        elif value in ["false", "f", "no", "n", "0"]:
            return False
        else:
            raise click.BadParameter(
                "Boolean value must be true/false, yes/no, t/f, y/n, or 1/0"
            )
    return value


# Validates that a client is associated with the logged-in sales collaborator.
def validate_client_by_sales(ctx, param, value):
    """
    Validates if the client is associated with the salesperson's account.

    Args:
        ctx (object): The click context object.
        param (str): The parameter name.
        value (int): The client ID.

    Returns:
        int: The validated client ID.

    Raises:
        click.BadParameter: If the client is not associated with the salesperson's
        account.
    """
    session = SessionLocal()
    client = Client.get_by_id(value, session)
    login_collaborator = get_login_collaborator(session=session)
    session.close()
    if login_collaborator.id != client.commercial_collaborator_id:
        raise click.BadParameter("Client must be associated with your account")
    return value


# Validates that the amount due is less than or equal to the total amount.
def validate_amount(ctx, param, value):
    """
    Validate the amount due against the total amount.

    Args:
        ctx (click.Context): The click context object.
        param (click.Parameter): The click parameter object.
        value (float): The amount due.

    Returns:
        float: The validated amount due.

    Raises:
        click.BadParameter: If the amount due is greater than the total amount.
    """
    total_amount = ctx.params.get("total_amount")
    if value > total_amount:
        raise click.BadParameter(
            "Amount due must be less than or equal to total amount."
        )
    return value


def validate_date(ctx, param, value):
    """
    Validate the date parameter.

    Args:
        ctx (click.Context): The click context.
        param (click.Parameter): The click parameter.
        value (str): The value to be validated.

    Returns:
        str: The validated date value.

    Raises:
        click.BadParameter: If the date is not in the correct format or if
        it is in the past.
    """
    try:
        date_format = "%Y-%m-%d %H:%M"
        date = datetime.strptime(value, date_format)
        if date < datetime.now():
            raise click.BadParameter("Date must be in the future")
        return value
    except ValueError:
        raise click.BadParameter("Date must be in the format yyyy-mm-dd HH:MM")


# Validates that the end date is after the start date.
def validate_end_date(ctx, param, value):
    """
    Validate the end date parameter.

    Args:
        ctx (click.Context): The click context.
        param (click.Parameter): The click parameter.
        value (str): The value of the end date.

    Returns:
        str: The validated end date.

    Raises:
        click.BadParameter: If the end date is before the start date.
    """
    validate_date(ctx, param, value)
    date_start = ctx.params.get("date_start")
    date_start = datetime.strptime(date_start, "%Y-%m-%d %H:%M")
    date_end = datetime.strptime(value, "%Y-%m-%d %H:%M")
    if date_end < date_start:
        raise click.BadParameter("End date must be after start date.")
    return value


# Validates that the number of attendees is a positive integer.
def validate_attendees(ctx, param, value):
    """
    Validate the number of attendees.

    Args:
        ctx (click.Context): The click context.
        param (click.Parameter): The click parameter.
        value (str): The value to be validated.

    Returns:
        int: The validated number of attendees.

    Raises:
        click.BadParameter: If the value is not a positive integer.
    """
    try:
        int(value)
    except ValueError:
        raise click.BadParameter("Attendees must be a positive integer")
    if value < 0:
        raise click.BadParameter("Attendees must be a positive integer")
    return value


# Validates that a client exists in the database.
def validate_client(ctx, param, value):
    """
    Validate the client ID provided.

    Args:
        ctx (click.Context): The click context.
        param (click.Parameter): The click parameter.
        value: The value of the client ID.

    Returns:
        The validated client ID.

    Raises:
        click.BadParameter: If the client ID is not found.
    """
    session = SessionLocal()
    client = Client.get_by_id(value, session)
    login_collaborator = get_login_collaborator(session)
    if str(login_collaborator.role) == "sales":
        if client.commercial_collaborator_id != login_collaborator.id:
            raise click.BadParameter("You are alowed to choose only your clients")
    session.close()
    if not client:
        raise click.BadParameter("Client not found")
    return value


def validate_event_id(ctx, param, value):
    """
    Validate the event ID.

    Args:
        ctx (click.Context): The click context.
        param (click.Parameter): The click parameter.
        value: The value of the event ID.

    Returns:
        The validated event ID.

    Raises:
        click.BadParameter: If the event is not found in the database.
    """
    session = SessionLocal()
    event = Event.get_by_id(value, session)
    login_collaborator = get_login_collaborator(session)
    if str(login_collaborator.role) == "support":
        if event.collaborator_support_id != login_collaborator.id:
            raise click.BadParameter("You are not allowed to update this event")
    if not event:
        raise click.BadParameter("Event not found")
    session.close()
    return value


# Validates that the logged-in support collaborator is assigned to the event.
def validate_event_assigned_to_support_id(ctx, param, value):
    """
    Validates if the event is assigned to the support ID of the
    logged-in collaborator.

    Args:
        ctx (click.Context): The click context.
        param (click.Parameter): The click parameter.
        value: The value to be validated.

    Returns:
        The validated value.

    Raises:
        click.BadParameter: If the event is not found or the logged-in
        collaborator is not allowed to update the event.
    """
    session = SessionLocal()
    login_collaborator = get_login_collaborator(session)
    event = Event.get_by_id(value, session)
    if not event:
        raise click.BadParameter("Event not found")
    if event.collaborator_support_id != login_collaborator.id:
        raise click.BadParameter("You are not allowed to update this event")
    session.close()
    return value


# Validates that a collaborator exists in the database.
def validate_collaborator(ctx, param, value):
    """
    Validate the collaborator by checking if it exists in the database.

    Args:
        ctx: The click context.
        param: The click parameter.
        value: The value of the collaborator ID.

    Returns:
        The validated collaborator ID.

    Raises:
        click.BadParameter: If the collaborator is not found in the database.
    """
    session = SessionLocal()
    collaborator = Collaborator.get_by_id(value, session)
    session.close()
    if not collaborator:
        raise click.BadParameter("Collaborator not found")
    return value


# Validates that a collaborator is a sales role.
def validate_commercial(ctx, param, value):
    """
    Validate the commercial parameter.

    Args:
        ctx (click.Context): The click context.
        param (click.Parameter): The click parameter.
        value: The value of the parameter.

    Returns:
        The validated value.

    Raises:
        click.BadParameter: If the commercial is not found or has an invalid role.
    """
    session = SessionLocal()
    collaborator = Collaborator.get_by_id(value, session)
    if not collaborator or str(collaborator.role) != "sales":
        raise click.BadParameter("commercial not found")
    session.close()
    return value


# Validates that a contract exists in the database.
def validate_contract(ctx, param, value):
    """
    Validates the contract by checking if it exists in the database.

    Args:
        ctx: The click context object.
        param: The click parameter object.
        value: The value of the contract ID to be validated.

    Returns:
        The validated contract ID.

    Raises:
        click.BadParameter: If the contract is not found in the database.
    """
    session = SessionLocal()
    found_contract = Contract.get_by_id(value, session)
    session.close()
    if not found_contract:
        raise click.BadParameter("Contract not found")
    return value


def validate_existing_contract_id(ctx, param, value):
    """
    Validates the contract ID.

    Args:
        ctx: The click context.
        param: The click parameter.
        value: The contract ID to be validated.

    Returns:
        The validated contract ID.

    Raises:
        click.BadParameter: If the contract is not found.
    """
    session = SessionLocal()
    found_contract = Contract.get_by_id(value, session)
    session.close()
    if not found_contract:
        raise click.BadParameter("Contract not found")
    return value


def validate_contract_id_is_signed(ctx, param, value):
    """
    Validates the contract ID.

    Args:
        ctx: The click context.
        param: The click parameter.
        value: The contract ID to be validated.

    Returns:
        The validated contract ID.

    Raises:
        click.BadParameter: If the contract is not found.
    """
    session = SessionLocal()
    found_contract = Contract.get_by_id(value, session)
    session.close()
    if not found_contract.status:
        raise click.BadParameter("Contract must be signed")
    return value


# Validates that a contract exists and is signed.
def validate_contract_id_existing_is_signed(ctx, param, value):
    """
    Validates the contract ID.

    Args:
        ctx: The click context.
        param: The click parameter.
        value: The contract ID to be validated.

    Returns:
        The validated contract ID.

    Raises:
        click.BadParameter: If the contract is not found or is not signed.
    """
    validate_existing_contract_id(ctx, param, value)
    validate_contract_is_assigned_to_another_event(ctx, param, value)
    validate_contract_id_is_signed(ctx, param, value)
    return value


# Validates that the logged-in collaborator is associated with the contract.
def validate_contract_by_collaborator(ctx, param, value):
    """
    Validates the contract by collaborator.

    Args:
        ctx (click.Context): The click context.
        param (click.Parameter): The click parameter.
        value: The contract value to be validated.

    Returns:
        The validated contract value.

    Raises:
        click.BadParameter: If the collaborator does not have
        permission on the contract.
    """
    session = SessionLocal()
    found_contract = Contract.get_by_id(value, session)
    validate_existing_contract_id(ctx, param, value)
    login_collaborator = get_login_collaborator(session)
    if str(login_collaborator.role) == "sales":
        if found_contract.commercial_collaborator_id != login_collaborator.id:
            raise click.BadParameter("You don't have permission on this contract")
    session.close()
    return value


def validate_contract_is_assigned_to_another_event(ctx, param, value):
    """
    Validates the contract by checking if it is assigned to another event.

    Args:
        ctx: The click context.
        param: The click parameter.
        value: The contract value to be validated.

    Returns:
        The validated contract value.

    Raises:
        click.BadParameter: If the contract is assigned to another event.
    """
    session = SessionLocal()
    found_contract = Contract.get_by_id(value, session)
    if found_contract.event:
        raise click.BadParameter("Contract is already assigned to an event")
    session.close()
    return value


def validate_contract_is_not_assigned_to_event(ctx, param, value):
    """
    Validates the contract by checking if it is not assigned to an event.

    Args:
        ctx: The click context.
        param: The click parameter.
        value: The contract value to be validated.

    Returns:
        The validated contract value.

    Raises:
        click.BadParameter: If the contract is assigned to an event.
    """
    session = SessionLocal()
    contract_id = ctx.params.get("id")
    found_contract = Contract.get_by_id(contract_id, session)
    if found_contract.event:
        raise click.BadParameter("Contract is already assigned "
                                 "to an event can't be unsigned")
    session.close()
    return value


def validate_contract_for_event(ctx, param, value):
    """
    Validates the contract by collaborator.

    Args:
        ctx (click.Context): The click context.
        param (click.Parameter): The click parameter.
        value: The contract value to be validated.

    Returns:
        The validated contract value.

    Raises:
        click.BadParameter: If the collaborator does not have
        permission on the contract.
    """
    validate_contract_by_collaborator(ctx, param, value)
    validate_contract_is_assigned_to_another_event(ctx, param, value)
    validate_contract_id_is_signed(ctx, param, value)
    return value


#  Validates that a role exists in the database.
def validate_role(ctx, param, value):
    """
    Validate the role value.

    Args:
        ctx: The click context.
        param: The click parameter.
        value: The value to be validated.

    Returns:
        The validated role value.

    Raises:
        click.BadParameter: If the role is not found.
    """
    session = SessionLocal()
    client = Role.get_by_id(value, session)
    session.close()
    if not client:
        raise click.BadParameter("Role not found")
    return value


# Validates that a collaborator is a support role.
def validate_support(ctx, param, value):
    """
    Validate if the given value corresponds to a valid support collaborator.

    Args:
        ctx (click.Context): The click context.
        param (click.Parameter): The click parameter.
        value: The value to be validated.

    Returns:
        The validated value.

    Raises:
        click.BadParameter: If the support collaborator is not found.
    """
    session = SessionLocal()
    collaborator = Collaborator.get_by_id(value, session)
    if not collaborator or str(collaborator.role) != "support":
        raise click.BadParameter("support not found")
    session.close()
    return value


# Validates that an employee number exists in the database.
def validate_employee_number(ctx, param, value):
    """
    Validates the employee number by checking if it exists in the database.

    Args:
        ctx: The click context object.
        param: The click parameter object.
        value: The value of the employee number to be validated.

    Returns:
        The validated employee number.

    Raises:
        click.BadParameter: If the employee number is not found in the database.
    """
    session = SessionLocal()
    collaborator = Collaborator.get_by_employee_number(value, session)
    if not collaborator:
        raise click.BadParameter("Employee_number not found")
    session.close()
    return value


def validate_employee_number_exist(ctx, param, value):
    """
    Validates the employee number by checking if it exists in the database.

    Args:
        ctx: The click context object.
        param: The click parameter object.
        value: The value of the employee number to be validated.

    Returns:
        The validated employee number.

    Raises:
        click.BadParameter: If the employee number exist.
    """
    session = SessionLocal()
    collaborator = Collaborator.get_by_employee_number(value, session)
    if collaborator:
        raise click.BadParameter("Employee_number already exist")
    session.close()
    return value
