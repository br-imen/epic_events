from datetime import datetime
from decimal import Decimal
import click
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
from controllers.contract_controller import create_contract_controller


@click.group()
def cli():
    pass


# Create collaborator
@cli.command()
@click.option(
    "--employee-number",
    prompt="Employee Number",
    help="The employee number of the collaborator.",
)
@click.option("--name", type=str, prompt="Name", help="The name of the collaborator.")
@click.option(
    "--email", type=str, prompt="Email", help="The email of the collaborator."
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
@click.option("--email", type=str, prompt="Email", help="The email of the user.")
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
def list_of_collaborators():
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
    "--email", type=str, prompt="Email", help="The email of the collaborator."
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
    required=True,
    help="Email address of the contact",
)
@click.option(
    "--phone-number",
    type=str,
    prompt="Phone number",
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
    "--contact-commercial",
    type=str,
    prompt="Contact commercial",
    required=True,
    help="Commercial contact person",
)
def create_client(full_name, email, phone_number, company_name, contact_commercial):
    """Create client"""
    create_client_controller(
        full_name, email, phone_number, company_name, contact_commercial
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
    required=True,
    help="Email address of the contact",
)
@click.option(
    "--phone-number",
    type=str,
    prompt="Phone number",
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
    "--contact-commercial",
    type=str,
    prompt="Contact commercial",
    required=True,
    help="Commercial contact person",
)
def update_client(id, full_name, email, phone_number, company_name, contact_commercial):
    """Update client"""
    update_client_controller(
        id, full_name, email, phone_number, company_name, contact_commercial
    )


# Create contract
@cli.command()
@click.option('--client_id', prompt="client id",type=int, required=True, help='Client ID')
@click.option('--commercial_contact', prompt="commercial_contact", type=str, help='Commercial Contact')
@click.option('--total_amount', prompt="total_amout",type=Decimal, required=True, help='Total Amount')
@click.option('--amount_due', prompt="amount_due", type=Decimal, required=True, help='Amount Due')
@click.option('--status', prompt="Signed",type=bool, required=True, help='Status')
def create_contract(client_id, commercial_contact, total_amount, amount_due, status):
    """Create contract"""
    create_contract_controller(client_id, commercial_contact, total_amount, amount_due, status)



if __name__ == "__main__":
    cli()
