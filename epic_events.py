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
from config.auth import has_permission, is_authenticated

# Create a custom Click context to store the subcommand name
class CustomContext(click.Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subcommand = None

class AuthGroup(click.Group):

    def invoke(self, ctx):
        session = SessionLocal()
        ctx.invoked_subcommand = ctx.protected_args[0] if ctx.protected_args else None
        print(f"Invoked subcommand: {ctx.invoked_subcommand}")
        if ctx.invoked_subcommand != "login":
            if not is_authenticated():
                print("Authentication required. Exiting.")
                exit(1)
            if not has_permission(command=ctx.invoked_subcommand, session=session):
                print("Permission denied.")
                exit(1)
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
    "--role-id", type=int, prompt="Role ID", help="The role ID of the collaborator."
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
    confirmation_prompt=True,
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
    help="The employee number of the collaborator.",
)
@click.option("--name", type=str, prompt="Name", help="The name of the collaborator.")
@click.option(
    "--email", type=str, prompt="Email", callback=validate_email, help="The email of the collaborator."
)
@click.option(
    "--role-id", type=int, prompt="Role ID", help="The role ID of the collaborator."
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
@click.option(
    "--commercial_collaborator_id",
    type=int,
    prompt="commercial_id",
    required=True,
    help="Commercial id",
)
def create_client(full_name, email, phone_number, company_name, commercial_collaborator_id):
    """Create client"""
    create_client_controller(
        full_name, email, phone_number, company_name, commercial_collaborator_id
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
@click.option(
    "--commercial_collaborator_id",
    type=int,
    prompt="commercial_id",
    required=True,
    help="Commercial id",
)
def update_client(id, full_name, email, phone_number, company_name, commercial_collaborator_id):
    """Update client"""
    update_client_controller(
        id, full_name, email, phone_number, company_name, commercial_collaborator_id
    )


# Create contract
@cli.command()
@click.option(
    "--client_id", prompt="client id", type=int, required=True, help="Client ID"
)
@click.option(
    "--commercial_collaborator_id",
    prompt="commercial_collaborator_id",
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
    "--amount_due", prompt="amount_due", type=DECIMAL, required=True, help="Amount Due"
)
@click.option("--status", prompt="is signed", type=bool, callback=validate_boolean, required=True, help="Status signed or not")
def create_contract(client_id, commercial_collaborator_id, total_amount, amount_due, status):
    """Create contract"""
    if amount_due > total_amount:
        raise click.BadParameter(
            "Amount due must be less than or equal to total amount."
        )
    create_contract_controller(
        client_id, commercial_collaborator_id, total_amount, amount_due, status
    )


# List contracts
@cli.command()
def list_contracts():
    """List contracts"""
    list_contracts_controller()


@cli.command()
@click.option(
    "--contract-id", prompt="contract id", type=int, required=True, help="Contract ID"
)
def delete_contract(contract_id):
    """Delete contract"""
    delete_contract_controller(contract_id)


# Update contracts
@cli.command()
@click.option("--id", prompt="contract id", type=int, required=True, help="Contract ID")
@click.option(
    "--client_id", prompt="client id", type=int, required=True, help="Client ID"
)
@click.option(
    "--commercial_collaborator_id",
    prompt="commercial_collaborator_id",
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
    "--amount_due", prompt="amount_due", type=DECIMAL, required=True, help="Amount Due"
)
@click.option("--status", prompt="is signed", type=bool, required=True, help="Status")
def update_contract(
    id, client_id, commercial_collaborator_id, total_amount, amount_due, status
):
    """Update contract"""
    if amount_due > total_amount:
        raise click.BadParameter(
            "Amount due must be less than or equal to total amount."
        )
    update_contract_controller(
        id, client_id, commercial_collaborator_id, total_amount, amount_due, status
    )


# Create event
@cli.command()
@click.option(
    "--client_id", prompt="Client ID", type=int, required=True, help="Client ID"
)
@click.option(
    "--contract_id", prompt="Contract ID", type=int, required=True, help="Contract ID"
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
    required=True,
    help="Start date and time",
)
@click.option(
    "--date_end",
    prompt="End Date (YYYY-MM-DD HH:MM:SS)",
    type=str,
    required=True,
    help="End date and time",
)
@click.option("--collaborator_support_id", prompt="Support id ",type=int,required=True,help="Support ID")
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
    help="Number of attendees",
)
@click.option(
    "--notes", prompt="Notes", type=str, required=False, help="Additional notes"
)
def create_event(
    client_id,
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
        "client_id": client_id,
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


# Update event
@cli.command()
@click.option("--id", prompt="Event ID", type=int, required=True, help="Event ID")
@click.option("--client_id", prompt="client_id", type=int, required=False, help="Client ID")
@click.option("--contract_id", prompt="contract_id", type=int, required=False, help="Contract ID")
@click.option(
    "--description", prompt="description", type=str, required=False, help="Description of the event"
)
@click.option(
    "--date_start",
    type=str, prompt="date start",
    required=False,
    help="Start date and time (YYYY-MM-DD HH:MM:SS)",
)
@click.option(
    "--date_end",
    type=str, prompt="date end",
    required=False,
    help="End date and time (YYYY-MM-DD HH:MM:SS)",
)
@click.option(
    "--collaborator_support_id",
    type=int, prompt="support contact id",
    required=False,
    help="support id",
)
@click.option("--location", type=str, prompt="location",required=False, help="Location of the event")
@click.option("--attendees", type=int, prompt="attendees",required=False, help="Number of attendees")
@click.option("--notes", type=str, prompt="notes",  required=False, help="Additional notes")
def update_event(
    id,
    client_id,
    contract_id,
    description,
    date_start,
    date_end,
    collaborator_support_id ,
    location,
    attendees,
    notes,
):
    """Update an event"""
    update_data = {
        "id": id,
        "client_id": client_id,
        "contract_id": contract_id,
        "description": description,
        "date_start": date_start,
        "date_end": date_end,
        "collaborator_support_id ": collaborator_support_id ,
        "location": location,
        "attendees": attendees,
        "notes": notes,
    }
    update_event_controller(**{k: v for k, v in update_data.items() if v is not None})


# Delete event
@cli.command()
@click.option("--id", prompt="Event ID", type=int, required=True, help="Event ID")
def delete_event(id):
    """Delete an event"""
    delete_event_controller(id)


# List events
@cli.command()
def list_events():
    """List events"""
    events = list_events_controller()


if __name__ == "__main__":
    cli()
