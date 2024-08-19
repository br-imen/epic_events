from decimal import Decimal, InvalidOperation
import click
from dotenv import load_dotenv
from pydantic import EmailStr
from config.database import SessionLocal
from config.logger import get_logger
from controllers.client_controller import (
    create_client_controller,
    delete_client_controller,
    list_clients_controller,
    update_client_controller,
)
from controllers.collaborator_controller import (
    create_collaborator_controller,
    authentication,
    logout_controller,
    list_collaborators_controller,
    delete_collaborator_controller,
    update_collaborator_controller,
    whoami_controller,
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
from config.auth import (
    get_login_collaborator,
    has_permission,
    is_authenticated,
)
from validators.click_validator import (
    validate_amount,
    validate_attendees,
    validate_boolean,
    validate_client,
    validate_client_by_sales,
    validate_commercial,
    validate_contract_by_collaborator,
    validate_contract_for_event,
    validate_contract_id_existing_is_signed,
    validate_contract_is_not_assigned_to_event,
    validate_date,
    validate_email,
    validate_email_exist,
    validate_employee_number,
    validate_employee_number_exist,
    validate_end_date,
    validate_event_assigned_to_support_id,
    validate_event_id,
    validate_phone_number,
    validate_role,
    validate_support,
)
from views.base_view import authentication_required_view, permission_denied_view

# Load environment variables from .env file
load_dotenv()


# Custom Click parameter type for validating non-negative decimal inputs.
class DecimalType(click.ParamType):
    """
    Custom parameter type for handling decimal values.
    """

    name = "decimal"

    def convert(self, value, param, ctx):
        """
        Converts the input value to a Decimal object.

        Args:
            value (str): The input value to be converted.
            param (click.Parameter): The parameter object.
            ctx (click.Context): The click context object.

        Returns:
            Decimal: The converted Decimal object.

        Raises:
            click.BadParameter: If the value is not a non-negative decimal or not
            a valid decimal.
        """
        try:
            dec_value = Decimal(value)
            if dec_value < 0:
                self.fail(f"{value} is not a non-negative decimal", param, ctx)
            return dec_value
        except InvalidOperation:
            self.fail(f"{value} is not a valid decimal", param, ctx)


DECIMAL = DecimalType()


# Create a custom Click context to store the subcommand name
class CustomContext(click.Context):
    """
    Custom context class for handling click commands.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subcommand = None


# Custom Click group that enforces authentication and permission checks
# before executing subcommands.
class AuthGroup(click.Group):
    """
    A custom click Group class that handles authentication and permission
    checks before invoking commands.
    """

    def invoke(self, ctx):
        """
        Overrides the invoke method of the click.Group class.
        Performs authentication and permission checks before invoking commands.
        """
        session = SessionLocal()
        ctx.invoked_subcommand = (
            ctx.protected_args[0] if ctx.protected_args else None
        )
        # Check if the invoked subcommand is in the list of available commands
        if (ctx.invoked_subcommand not in self.commands and
                ctx.invoked_subcommand not in ("update-event", )):
            # If not, print an error message and return
            click.echo(f"Error: Command '{ctx.invoked_subcommand}' "
                       "is not a valid command.")
            click.echo("Try 'epic_events.py --help' for help.")
            ctx.exit(1)

        if ctx.invoked_subcommand not in ("login", "logout", "whoami"):
            if not is_authenticated():
                authentication_required_view()
                exit(1)
            if not has_permission(command=ctx.invoked_subcommand, session=session):
                permission_denied_view()
                exit(1)
        if ctx.invoked_subcommand == "update-event":
            login_collaborator = get_login_collaborator(
                session
            )  # Replace with actual method to get the collaborator
            if str(login_collaborator.role) == "management":
                ctx.protected_args = [
                    "update-event-management"
                ] + ctx.protected_args[1:]
            elif str(login_collaborator.role) == "support":
                ctx.protected_args = ["update-event-support"] + ctx.protected_args[
                    1:
                ]
            ctx.invoked_subcommand = ctx.protected_args[0]
        super().invoke(ctx)


@click.group(cls=AuthGroup)
def cli():
    """
    This function represents the command-line interface for the Epic Events
    application.
    It serves as the entry point for executing various commands and interacting with
    the application.
    """
    pass


# Create collaborator
@cli.command()
@click.option(
    "--employee-number",
    prompt="Employee Number",
    callback=validate_employee_number_exist,
    help="The employee number of the collaborator.",
)
@click.option(
    "--name", type=str, prompt="Name", help="The name of the collaborator."
)
@click.option(
    "--email",
    type=EmailStr,
    callback=validate_email_exist,
    prompt="Email",
    help="The email of the collaborator.",
)
@click.option(
    "--role-id",
    type=int,
    callback=validate_role,
    prompt="Role ID",
    help="The role ID of the collaborator.",
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
@click.option(
    "--email",
    type=str,
    prompt="Email",
    callback=validate_email,
    help="The email of the user.",
)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    help="The password of the user.",
)
def login(email, password):
    """Login"""
    authentication(email, password)


# Logout
@cli.command()
def logout():
    """Logout"""
    logout_controller()


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
    callback=validate_employee_number,
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
@click.option(
    "--name", type=str, prompt="Name", help="The name of the collaborator."
)
@click.option(
    "--email",
    type=str,
    prompt="Email",
    callback=validate_email_exist,
    help="The email of the collaborator.",
)
@click.option(
    "--role-id",
    type=int,
    callback=validate_role,
    prompt="Role ID",
    help="The role ID of the collaborator.",
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
    create_client_controller(full_name, email, phone_number, company_name)


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
@click.option(
    "--commercial-collaborator-id",
    type=str,
    prompt="commercial collaborator id",
    callback=validate_commercial,
    required=True,
    help="Id for the commercial collaborator responsible for the client",
)
def update_client(id, full_name, email, phone_number, company_name,
                  commercial_collaborator_id):
    """Update client"""
    update_client_controller(
        id, full_name, email, phone_number, company_name, commercial_collaborator_id
    )


# Create contract
@cli.command()
@click.option(
    "--client_id",
    prompt="client id",
    callback=validate_client,
    type=int,
    required=True,
    help="Client ID",
)
@click.option(
    "--total_amount",
    prompt="total_amout",
    type=DECIMAL,
    required=True,
    help="Total Amount",
)
@click.option(
    "--amount_due",
    prompt="amount_due",
    callback=validate_amount,
    type=DECIMAL,
    required=True,
    help="Amount Due",
)
@click.option(
    "--status",
    prompt="is signed",
    type=bool,
    callback=validate_boolean,
    required=True,
    help="Status signed or not",
)
def create_contract(
    client_id, total_amount, amount_due, status
):
    """Create contract"""
    create_contract_controller(
        client_id, total_amount, amount_due, status
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
    "--contract-id",
    prompt="contract id",
    callback=validate_contract_by_collaborator,
    type=int,
    required=True,
    help="Contract ID",
)
def delete_contract(contract_id):
    """Delete contract"""
    delete_contract_controller(contract_id)


# Update contract
@cli.command()
@click.option(
    "--id",
    prompt="contract id",
    type=int,
    callback=validate_contract_by_collaborator,
    required=True,
    help="Contract ID",
)
@click.option(
    "--client_id",
    prompt="client id",
    type=int,
    callback=validate_client,
    required=True,
    help="Client ID",
)
@click.option(
    "--total_amount",
    prompt="total_amout",
    type=DECIMAL,
    required=True,
    help="Total Amount",
)
@click.option(
    "--amount_due",
    prompt="amount_due",
    callback=validate_amount,
    type=DECIMAL,
    required=True,
    help="Amount Due",
)
@click.option(
    "--status",
    prompt="is signed",
    callback=validate_contract_is_not_assigned_to_event,
    type=bool,
    required=True,
    help="Status"
)
def update_contract(
    id, client_id, total_amount, amount_due, status
):
    """Update contract"""
    update_contract_controller(
        id,
        client_id,
        total_amount,
        amount_due,
        status,
    )


# Create event
@cli.command()
@click.option(
    "--contract_id",
    prompt="Contract ID",
    callback=validate_contract_for_event,
    type=int,
    required=True,
    help="Contract ID",
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
    prompt="Start Date (YYYY-MM-DD HH:MM)",
    type=str,
    callback=validate_date,
    required=True,
    help="Start date and time",
)
@click.option(
    "--date_end",
    prompt="End Date (YYYY-MM-DD HH:MM)",
    type=str,
    callback=validate_end_date,
    required=True,
    help="End date and time",
)
@click.option(
    "--location",
    prompt="Location",
    type=str,
    required=True,
    help="Location of the event",
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
    "--notes",
    prompt="Notes",
    type=str,
    required=False,
    help="Additional notes",
)
def create_event(
    contract_id,
    description,
    date_start,
    date_end,
    location,
    attendees,
    notes,
):
    """Create an event"""
    event_data = {
        "contract_id": contract_id,
        "description": description,
        "date_start": date_start,
        "date_end": date_end,
        "location": location,
        "attendees": attendees,
        "notes": notes,
    }
    create_event_controller(**event_data)


# Update event management
@click.command()
@click.option(
    "--id",
    prompt="Event ID",
    type=int,
    callback=validate_event_id,
    required=True,
    help="Event ID",
)
@click.option(
    "--collaborator_support_id",
    type=int,
    prompt="support contact id",
    callback=validate_support,
    required=True,
    help="support id",
)
def update_event_management(id, collaborator_support_id):
    """Update event for manager role"""
    update_data = {
        "id": id,
        "collaborator_support_id": collaborator_support_id,
    }
    update_event_controller(**update_data)


# Update event support
@click.command()
@click.option(
    "--id",
    prompt="Event ID",
    type=int,
    callback=validate_event_assigned_to_support_id,
    required=True,
    help="Event ID",
)
@click.option(
    "--contract_id",
    prompt="Contract ID",
    callback=validate_contract_id_existing_is_signed,
    type=int,
    required=False,
    help="Contract ID",
)
@click.option(
    "--description",
    prompt="Description",
    type=str,
    required=False,
    help="Description of the event",
)
@click.option(
    "--date_start",
    type=str,
    prompt="Date start",
    callback=validate_date,
    required=False,
    help="Start date and time (YYYY-MM-DD HH:MM:SS)",
)
@click.option(
    "--date_end",
    type=str,
    prompt="Date end",
    callback=validate_end_date,
    required=False,
    help="End date and time (YYYY-MM-DD HH:MM:SS)",
)
@click.option(
    "--collaborator_support_id",
    type=int,
    prompt="Support contact id",
    callback=validate_support,
    required=False,
    help="Support id",
)
@click.option(
    "--location",
    type=str,
    prompt="Location",
    required=False,
    help="Location of the event",
)
@click.option(
    "--attendees",
    type=int,
    callback=validate_attendees,
    prompt="Attendees",
    required=False,
    help="Number of attendees",
)
@click.option(
    "--notes",
    type=str,
    prompt="Notes",
    required=False,
    help="Additional notes",
)
def update_event_support(
    id,
    contract_id,
    description,
    date_start,
    date_end,
    collaborator_support_id,
    location,
    attendees,
    notes,
):
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
        raise click.BadParameter(
            "Can't use both with_no_support and assigned_to_me together"
        )
    if with_no_support:
        filters.append("with_no_support")
    elif assigned_to_me:
        filters.append("assigned_to_me")
    list_events_controller(
        filters,
    )


# List events
@cli.command()
def whoami():
    """Print the current user"""
    whoami_controller()


if __name__ == "__main__":
    logger = get_logger() # noqa

    cli()
