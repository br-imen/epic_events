from datetime import datetime
import re

import click

from config.auth import get_login_collaborator
from config.database import SessionLocal
from models.client import Client
from models.collaborator import Collaborator, Role
from models.contract import Contract
from models.event import Event


def validate_email(ctx, param, value):
    # Simple regex for validating an email address
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
        raise click.BadParameter("Invalid email address format")
    return value


# Validate_phone_number
def validate_phone_number(ctx, param, value):
    if not re.match(r"^(\+33|0)\d{9}$", value):
        raise click.BadParameter("Invalid phone number format")
    return value


# Validate bool input status:
def validate_boolean(ctx, param, value):
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


def validate_client_by_sales(ctx, param, value):
    session = SessionLocal()
    client = Client.get_by_id(value, session)
    login_collaborator = get_login_collaborator(session=session)
    session.close()
    if login_collaborator.id != client.commercial_collaborator_id:
        raise click.BadParameter("Client must be associated with your account")
    return value


def validate_amount(ctx, param, value):
    total_amount = ctx.params.get("total_amount")
    if value > total_amount:
        raise click.BadParameter(
            "Amount due must be less than or equal to total amount."
        )
    return value


def validate_date(ctx, param, value):
    try:
        date_format = "%Y-%m-%d %H:%M"
        date = datetime.strptime(value, date_format)
        if date < datetime.now():
            raise click.BadParameter("Date must be in the future")
        return value
    except ValueError:
        raise click.BadParameter("Date must be in the format yyyy-mm-dd HH:MM")


def validate_end_date(ctx, param, value):
    validate_date(ctx, param, value)
    date_start = ctx.params.get("date_start")
    date_start = datetime.strptime(date_start, "%Y-%m-%d %H:%M")
    date_end = datetime.strptime(value, "%Y-%m-%d %H:%M")
    if date_end < date_start:
        raise click.BadParameter("End date must be after start date.")
    return value


def validate_attendees(ctx, param, value):
    try:
        int(value)
    except ValueError:
        raise click.BadParameter("Attendees must be a positive integer")
    if value < 0:
        raise click.BadParameter("Attendees must be a positive integer")
    return value


def validate_client(ctx, param, value):
    session = SessionLocal()
    client = Client.get_by_id(value, session)
    session.close()
    if not client:
        raise click.BadParameter("Client not found")
    return value


def validate_event_id(ctx, param, value):
    session = SessionLocal()
    event = Event.get_by_id(value, session)
    if not event:
        raise click.BadParameter("Event not found")
    session.close()
    return value


def validate_event_assigned_to_support_id(ctx, param, value):
    session = SessionLocal()
    login_collaborator = get_login_collaborator(session)
    event = Event.get_by_id(value, session)
    if not event:
        raise click.BadParameter("Event not found")
    if event.collaborator_support_id != login_collaborator.id:
        raise click.BadParameter("You are not allowed to update this event")
    session.close()
    return value


def validate_collaborator(ctx, param, value):
    session = SessionLocal()
    collaborator = Collaborator.get_by_id(value, session)
    session.close()
    if not collaborator:
        raise click.BadParameter("Collaborator not found")
    return value


def validate_commercial(ctx, param, value):
    session = SessionLocal()
    collaborator = Collaborator.get_by_id(value, session)
    if not collaborator or str(collaborator.role) != "sales":
        raise click.BadParameter("commercial not found")
    session.close()
    return value


def validate_contract(ctx, param, value):
    session = SessionLocal()
    found_contract = Contract.get_by_id(value, session)
    session.close()
    if not found_contract:
        raise click.BadParameter("Contract not found")
    return value


def validate_contract_id(ctx, param, value):
    session = SessionLocal()
    found_contract = Contract.get_by_id(value, session)
    session.close()
    if not found_contract:
        raise click.BadParameter("Contract not found")
    if not found_contract.status:
        raise click.BadParameter("Contract must be signed")
    return value


def validate_contract_by_collaborator(ctx, param, value):
    session = SessionLocal()
    found_contract = Contract.get_by_id(value, session)
    validate_contract_id(ctx, param, value)
    login_collaborator = get_login_collaborator(session)
    if str(login_collaborator.role) == "sales":
        if found_contract.commercial_collaborator_id != login_collaborator.id:
            raise click.BadParameter("You don't have permission on this contract")
    session.close()
    return value


def validate_role(ctx, param, value):
    session = SessionLocal()
    client = Role.get_by_id(value, session)
    session.close()
    if not client:
        raise click.BadParameter("Role not found")
    return value


def validate_support(ctx, param, value):
    session = SessionLocal()
    collaborator = Collaborator.get_by_id(value, session)
    if not collaborator or str(collaborator.role) != "support":
        raise click.BadParameter("support not found")
    session.close()
    return value


def validate_employee_number(ctx, param, value):
    session = SessionLocal()
    collaborator = Collaborator.get_by_employee_number(value, session)
    if not collaborator:
        raise click.BadParameter("Employee_number not found")
    session.close()
    return value
