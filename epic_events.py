import click
from controllers.collaborator_controller import create_collaborator_controller, authentication, list_collaborators_controller, delete_collaborator_controller, update_collaborator_controller

@click.group()
def cli():
    pass

# Create collaborator
@cli.command()
@click.option("--employee-number", prompt="Employee Number", help="The employee number of the collaborator.")
@click.option("--name", prompt="Name", help="The name of the collaborator.")
@click.option("--email", prompt="Email", help="The email of the collaborator.")
@click.option("--role-id", prompt="Role ID", help="The role ID of the collaborator.")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="The password of the collaborator.",
)
def create_collaborator(employee_number,name,email,role_id,password):
    """Create a new collaborator"""
    create_collaborator_controller(employee_number,name,email,role_id,password)


# Login 
@cli.command()
@click.option("--email", prompt="Email", help="The email of the user.")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="The password of the user.",
)
def login(email, password):
    """Login"""
    authentication(email,password)


# List_collaborators
@cli.command()
def list_of_collaborators():
    """List of collaborators"""
    list_collaborators_controller()


# delete_collaborators
@cli.command()
@click.option("--employee-number", prompt="Employee Number", help="The employee number of the collaborator.")
def delete_collaborator(employee_number):
    """Delete collaborator"""
    delete_collaborator_controller(employee_number)


# update_collaborators
@cli.command()
@click.option("--employee-number", prompt="Employee Number", help="The employee number of the collaborator.")
@click.option("--name", prompt="Name", help="The name of the collaborator.")
@click.option("--email", prompt="Email", help="The email of the collaborator.")
@click.option("--role-id", prompt="Role ID", help="The role ID of the collaborator.")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="The password of the collaborator.",
)
def update_collaborator(employee_number,name,email,role_id,password):
    """Update collaborator"""
    update_collaborator_controller(employee_number,name,email,role_id,password)

if __name__ == '__main__':
    cli()