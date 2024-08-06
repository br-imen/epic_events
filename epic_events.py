from datetime import datetime
from decimal import Decimal, InvalidOperation
import click
import re
from pydantic import EmailStr
from config.database import SessionLocal
from controllers.client_controller import (
    create_client_controller,
    delete_client_controller,
    list_clients_controller,
    update_client_controller,
)
from controllers.collaborator_controller import (
    create_collaborator_controller,
    authentication,
    list_collaborators_controller,
    delete_collaborator_controller,
    update_collaborator_controller,
)
from controllers.contract_controller import (
    create_contract_controller,
    delete_contract_controller,
    list_contracts_controller,
    update_contract_controller,
)
from controllers.event_controller import (
    create_event_controller,
    delete_event_controller,
    list_events_controller,
    update_event_controller,
)
from config.auth import get_login_collaborator, has_permission, is_authenticated
from models.client import Client
from models.collaborator import Collaborator, Role
from models.contract import Contract
from models.event import Event

# Create a custom Click context to store the subcommand name
class CustomContext(click.Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subcommand = None

class AuthGroup(click.Group):

    def invoke(self, ctx):
        session = SessionLocal()
        ctx.invoked_subcommand = ctx.protected_args[0] if ctx.protected_args else None
        if ctx.invoked_subcommand not in ("login", ):
            if not is_authenticated():
                print("Authentication required. Exiting.")
                exit(1)
            if not has_permission(command=ctx.invoked_subcommand, session=session):
                print("Permission denied.")
                exit(1)
        if ctx.invoked_subcommand == "update-event":
            login_collaborator = get_login_collaborator(session)  # Replace with actual method to get the collaborator
            if str(login_collaborator.role) == "management":
                ctx.protected_args = ["update-event-management"] + ctx.protected_args[1:]
            elif str(login_collaborator.role) == "support":
                ctx.protected_args = ["update-event-support"] + ctx.protected_args[1:]
            ctx.invoked_subcommand = ctx.protected_args[0]
        super().invoke(ctx)
        
@click.group(cls=AuthGroup)
def cli():
    pass

# Validate email
def validate_email(ctx, param, value):
    # Simple regex for validating an email address
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
        raise click.BadParameter('Invalid email address format')
    return value

# Validate_phone_number
def validate_phone_number(ctx, param, value):
    if not re.match(r'^(\+33|0)\d{9}$', value):
        raise click.BadParameter('Invalid phone number format')
    return value


# Validation for contract
class DecimalType(click.ParamType):
    name = "decimal"

    def convert(self, value, param, ctx):
        try:
            dec_value = Decimal(value)
            if dec_value < 0:
                self.fail(f"{value} is not a non-negative decimal", param, ctx)
            return dec_value
        except InvalidOperation:
            self.fail(f"{value} is not a valid decimal", param, ctx)


DECIMAL = DecimalType()


# Validate bool input status:
def validate_boolean(ctx, param, value):
    if isinstance(value, str):
        value = value.lower()
        if value in ['true', 't', 'yes', 'y', '1']:
            return True
        elif value in ['false', 'f', 'no', 'n', '0']:
            return False
        else:
            raise click.BadParameter('Boolean value must be true/false, yes/no, t/f, y/n, or 1/0')
    return value

def validate_client_by_sales(ctx, param, value):
    session = SessionLocal()
    client = Client.get_by_id(value, session)
    login_collaborator = get_login_collaborator(session=session)
    session.close()
    if login_collaborator.id != client.commercial_collaborator_id:
        raise click.BadParameter('Client must be associated with your account')
    return value

def validate_amount(ctx, param, value):
    total_amount = ctx.params.get('total_amount')
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
            raise click.BadParameter(
            "Date must be in the future"
        )
        return value
    except ValueError:
        raise click.BadParameter(
            "Date must be in the format yyyy-mm-dd HH:MM"
        )
    
def validate_end_date(ctx, param, value):
    validate_date(ctx, param, value)
    date_start = ctx.params.get('date_start')
    date_start = datetime.strptime(date_start, "%Y-%m-%d %H:%M")
    date_end = datetime.strptime(value, "%Y-%m-%d %H:%M")
    if date_end < date_start:
        raise click.BadParameter(
            "End date must be after start date."
        )
    return value

def validate_attendees(ctx, param, value):
    try:
        int(value)
    except ValueError:
        raise click.BadParameter(
            "Attendees must be a positive integer"
        )
    if value < 0:
        raise click.BadParameter(
            "Attendees must be a positive integer"
        )
    return value

def validate_client(ctx, param, value):
    session = SessionLocal()
    client = Client.get_by_id(value, session)
    session.close()
    if not client:
        raise click.BadParameter('Client not found')
    return value

def validate_event_id(ctx, param, value):
    session = SessionLocal()
    event = Event.get_by_id(value, session)
    if not event:
        raise click.BadParameter('Event not found')
    session.close()
    return value

def validate_event_assigned_to_support_id(ctx, param, value):
    session = SessionLocal()
    login_collaborator = get_login_collaborator(session)
    event = Event.get_by_id(value, session)
    if not event:
        raise click.BadParameter('Event not found')
    if event.collaborator_support_id != login_collaborator.id:
        raise click.BadParameter('You are not allowed to update this event')
    session.close()
    return value

def validate_collaborator(ctx, param, value):
    session = SessionLocal()
    collaborator = Collaborator.get_by_id(value, session)
    session.close()
    if not collaborator:
        raise click.BadParameter('Collaborator not found')
    return value

def validate_commercial(ctx, param, value):
    session = SessionLocal()
    collaborator = Collaborator.get_by_id(value, session)
    if not collaborator or str(collaborator.role) != "sales":
        raise click.BadParameter('commercial not found')    
    session.close()
    return value

def validate_contract(ctx, param, value):
    session = SessionLocal()
    found_contract = Contract.get_by_id(value, session)
    session.close()
    if not found_contract:
        raise click.BadParameter('Contract not found')
    return value

def validate_contract_id(ctx, param, value):
    session = SessionLocal()
    found_contract = Contract.get_by_id(value, session)
    session.close()
    if not found_contract:
        raise click.BadParameter('Contract not found')
    if not found_contract.status:
        raise click.BadParameter('Contract must be signed')
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
        raise click.BadParameter('Role not found')
    return value

def validate_support(ctx, param, value):
    session = SessionLocal()
    collaborator = Collaborator.get_by_id(value, session)
    if not collaborator or str(collaborator.role) != "support":
        raise click.BadParameter('support not found')    
    session.close()
    return value

def validate_employee_number(ctx, param, value):
    session = SessionLocal()
    collaborator = Collaborator.get_by_employee_number(value, session)
    if not collaborator:
        raise click.BadParameter('Employee_number not found')    
    session.close()
    return value

# Create collaborator
@cli.command()
@click.option(
    "--employee-number",
    prompt="Employee Number",
    help="The employee number of the collaborator.",
)
@click.option("--name", type=str, prompt="Name", help="The name of the collaborator.")
@click.option(
    "--email", type=EmailStr, callback=validate_email, prompt="Email", help="The email of the collaborator."
)
@click.option(
    "--role-id", type=int, callback=validate_role, prompt="Role ID", help="The role ID of the collaborator."
)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="The password of the collaborator.",
)
def create_collaborator(employee_number, name, email, role_id, password):
    """Create collaborator"""
    create_collaborator_controller(employee_number, name, email, role_id, password)

# Login
@cli.command()
@click.option("--email", type=str, prompt="Email", callback=validate_email, help="The email of the user.")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,

    help="The password of the user.",
)
def login(email, password):
    """Login"""
    authentication(email, password)


# List_collaborators
@cli.command()
def list_collaborators():
    """List collaborators"""
    list_collaborators_controller()


# Delete collaborators
@cli.command()
@click.option(
    "--employee-number",
    type=int,
    callback=validate_collaborator,
    prompt="Employee Number",
    help="The employee number of the collaborator.",
)
def delete_collaborator(employee_number):
    """Delete collaborator"""
    delete_collaborator_controller(employee_number)


# Update collaborators
@cli.command()
@click.option(
    "--employee-number",
    prompt="Employee Number",
    type=int,
    callback=validate_employee_number,
    help="The employee number of the collaborator.",
)
@click.option("--name", type=str, prompt="Name", help="The name of the collaborator.")
@click.option(
    "--email", type=str, prompt="Email", callback=validate_email, help="The email of the collaborator."
)
@click.option(
    "--role-id", type=int, callback=validate_role, prompt="Role ID", help="The role ID of the collaborator."
)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="The password of the collaborator.",
)
def update_collaborator(employee_number, name, email, role_id, password):
    """Update collaborator"""
    update_collaborator_controller(employee_number, name, email, role_id, password)


# Create client
@cli.command()
@click.option(
    "--full-name",
    type=str,
    prompt="Full-name",
    required=True,
    help="Full name of the contact",
)
@click.option(
    "--email",
    type=str,
    prompt="Email",
    callback=validate_email,
    required=True,
    help="Email address of the contact",
)
@click.option(
    "--phone-number",
    type=str,
    prompt="Phone number",
    callback=validate_phone_number,
    required=True,
    help="Phone number of the contact",
)
@click.option(
    "--company-name",
    type=str,
    prompt="Company name",
    required=True,
    help="Company name of the contact",
)
def create_client(full_name, email, phone_number, company_name):
    """Create client"""
    create_client_controller(
        full_name, email, phone_number, company_name
    )


# List clients
@cli.command()
def list_clients():
    """List clients"""
    list_clients_controller()


@cli.command()
@click.option(
    "--client_id",
    type=int,
    prompt="id client",
    required=True,
    callback=validate_client_by_sales,
    help="the id client to delete",
)
# Delete client
def delete_client(client_id):
    """Delete client"""
    delete_client_controller(client_id)


# Update client
@cli.command()
@click.option(
    "--id",
    type=int,
    prompt="id-client",
    callback=validate_client_by_sales,
    required=True,
    help="Id client",
)
@click.option(
    "--full-name",
    type=str,
    prompt="Full-name",
    required=True,
    help="Full name of the contact",
)
@click.option(
    "--email",
    type=str,
    prompt="Email",
    callback=validate_email,
    required=True,
    help="Email address of the contact",
)
@click.option(
    "--phone-number",
    type=str,
    prompt="Phone number",
    callback=validate_phone_number,
    required=True,
    help="Phone number of the contact",
)
@click.option(
    "--company-name",
    type=str,
    prompt="Company name",
    required=True,
    help="Company name of the contact",
)
def update_client(id, full_name, email, phone_number, company_name):
    """Update client"""
    update_client_controller(
        id, full_name, email, phone_number, company_name
    )


# Create contract
@cli.command()
@click.option(
    "--client_id", prompt="client id", callback=validate_client, type=int, required=True, help="Client ID"
)
@click.option(
    "--commercial_collaborator_id",
    prompt="commercial_collaborator_id",
    callback=validate_commercial,
    type=int,
    help="Commercial id",
)
@click.option(
    "--total_amount",
    prompt="total_amout",
    type=DECIMAL,
    required=True,
    help="Total Amount",
)
@click.option(
    "--amount_due", prompt="amount_due", callback=validate_amount, type=DECIMAL, required=True, help="Amount Due"
)
@click.option("--status", prompt="is signed", type=bool, callback=validate_boolean, required=True, help="Status signed or not")
def create_contract(client_id, commercial_collaborator_id, total_amount, amount_due, status):
    """Create contract"""
    create_contract_controller(
        client_id, commercial_collaborator_id, total_amount, amount_due, status
    )


# List contracts
@click.option(
    "--unpaid",
    is_flag=True,
    help="unpaid contract",
)
@click.option(
    "--unsigned",
    is_flag=True,
    help="unsigned contract",
)
@cli.command()
def list_contracts(unpaid, unsigned):
    """List contracts"""
    filters = []
    if unpaid:
        filters.append("unpaid")
    if unsigned:
        filters.append("unsigned")
    list_contracts_controller(filters=filters)


# Delete contracts
@cli.command()
@click.option(
    "--contract-id", prompt="contract id", callback=validate_contract_by_collaborator, type=int, required=True, help="Contract ID"
)
def delete_contract(contract_id):
    """Delete contract"""
    delete_contract_controller(contract_id)


# Update contracts
@cli.command()
@click.option("--id", prompt="contract id", type=int, callback=validate_contract_by_collaborator, required=True, help="Contract ID")
@click.option(
    "--client_id", prompt="client id", type=int, callback=validate_client, required=True, help="Client ID"
)
@click.option(
    "--commercial_collaborator_id",
    prompt="commercial_collaborator_id",
    type=int,
    callback=validate_commercial,
    help="Commercial id",
)
@click.option(
    "--total_amount",
    prompt="total_amout",
    type=DECIMAL,
    required=True,
    help="Total Amount",
)
@click.option(
    "--amount_due", prompt="amount_due", callback=validate_amount, type=DECIMAL, required=True, help="Amount Due"
)
@click.option("--status", prompt="is signed", type=bool, required=True, help="Status")
def update_contract(
    id, client_id, commercial_collaborator_id, total_amount, amount_due, status
):
    """Update contract"""
    update_contract_controller(
        id, client_id, commercial_collaborator_id, total_amount, amount_due, status
    )


# Create event
@cli.command()
@click.option(
    "--contract_id", prompt="Contract ID", callback=validate_contract_id, type=int, required=True, help="Contract ID"
)
@click.option(
    "--description",
    prompt="Description",
    type=str,
    required=True,
    help="Description of the event",
)
@click.option(
    "--date_start",
    prompt="Start Date (YYYY-MM-DD HH:MM:SS)",
    type=str,
    callback=validate_date,
    required=True,
    help="Start date and time",
)
@click.option(
    "--date_end",
    prompt="End Date (YYYY-MM-DD HH:MM:SS)",
    type=str,
    callback=validate_end_date,
    required=True,
    help="End date and time",
)
@click.option("--collaborator_support_id", prompt="Support id ", callback=validate_support, type=int, help="Support ID")
@click.option(
    "--location",
    prompt="Location",
    type=str,
    required=True,
    help="Location of the event"
)
@click.option(
    "--attendees",
    prompt="Number of Attendees",
    type=int,
    required=True,
    callback=validate_attendees,
    help="Number of attendees",
)
@click.option(
    "--notes", prompt="Notes", type=str, required=False, help="Additional notes"
)
def create_event(
    contract_id,
    description,
    date_start,
    date_end,
    collaborator_support_id,
    location,
    attendees,
    notes,
):
    """Create an event"""
    event_data = {
        "contract_id": contract_id,
        "description": description,
        "date_start":date_start ,
        "date_end": date_end,
        "collaborator_support_id": collaborator_support_id,
        "location": location,
        "attendees": attendees,
        "notes": notes,
    }
    create_event_controller(**event_data)

@click.command()
@click.option("--id", prompt="Event ID", type=int, callback=validate_event_id, required=True, help="Event ID")
@click.option("--collaborator_support_id", type=int, prompt="support contact id", callback=validate_support, required=True, help="support id")
def update_event_management(id, collaborator_support_id):
    """Update event for manager role"""
    update_data = {
        "id": id,
        "collaborator_support_id": collaborator_support_id
    }
    update_event_controller(**update_data)

@click.command()
@click.option("--id", prompt="Event ID", type=int, callback=validate_event_assigned_to_support_id, required=True, help="Event ID")
@click.option("--contract_id", prompt="Contract ID", callback=validate_contract_id, type=int, required=False, help="Contract ID")
@click.option("--description", prompt="Description", type=str, required=False, help="Description of the event")
@click.option("--date_start", type=str, prompt="Date start", callback=validate_date, required=False, help="Start date and time (YYYY-MM-DD HH:MM:SS)")
@click.option("--date_end", type=str, prompt="Date end", callback=validate_end_date, required=False, help="End date and time (YYYY-MM-DD HH:MM:SS)")
@click.option("--collaborator_support_id", type=int, prompt="Support contact id", callback=validate_support, required=False, help="Support id")
@click.option("--location", type=str, prompt="Location", required=False, help="Location of the event")
@click.option("--attendees", type=int, callback=validate_attendees, prompt="Attendees", required=False, help="Number of attendees")
@click.option("--notes", type=str, prompt="Notes", required=False, help="Additional notes")
def update_event_support(id, contract_id, description, date_start, date_end, collaborator_support_id, location, attendees, notes):
    """Update event for support role"""
    update_data = {
        "id": id,
        "contract_id": contract_id,
        "description": description,
        "date_start": date_start,
        "date_end": date_end,
        "collaborator_support_id": collaborator_support_id,
        "location": location,
        "attendees": attendees,
        "notes": notes,
    }
    update_data = {k: v for k, v in update_data.items() if v is not None}
    update_event_controller(**update_data)

cli.add_command(update_event_management)
cli.add_command(update_event_support)

# Delete event
@cli.command()
@click.option("--id", prompt="Event ID", type=int, required=True, help="Event ID")
def delete_event(id):
    """Delete an event"""
    delete_event_controller(id)


# List events
@cli.command()
@click.option("--with_no_support", is_flag=True, help="is it linked to a support")
@click.option("--assigned_to_me", is_flag=True, help="is it assigned to you")
def list_events(with_no_support, assigned_to_me):
    """List events"""
    filters = []
    if with_no_support and assigned_to_me:
        raise click.BadParameter("Can't use both with_no_support and assigned_to_me together")
    if with_no_support:
        filters.append("with_no_support")
    elif assigned_to_me:
        filters.append("assigned_to_me")
    list_events_controller(filters, )


if __name__ == "__main__":
    cli()
