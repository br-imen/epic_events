import logging


def success_login_view():
    print("Login successful!")


def success_logout_view():
    print("Logout successful!")


def error_invalid_email_password_view():
    print("Invalid email or password.")
    logging.error("Invalid email or password.")


def success_create_collaborator_view():
    print("Collaborator successfully created")
    logging.info("Collaborator successfully created")


def validation_error_view(e):
    print("Validation error:", e)
    logging.error(e)


def list_collaborators_view(collaborators):
    for collaborator in collaborators:
        print(collaborator)


def success_delete_collaborator_view():
    print("Collaborator successfully deleted")
    logging.info("Collaborator successfully deleted")


def error_collaborator_non_found_view():
    print("Collaborator doesn't exist")
    logging.error("Collaborator doesn't exist")


def success_update_collaborator_view():
    print("Collaborator updated")
    logging.info("Collaborator updated")
