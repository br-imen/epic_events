from config.logger import get_logger


logger = get_logger()


def success_login_view():
    print("Login successful!")


def success_logout_view():
    print("Logout successful!")


def error_invalid_email_password_view(email):
    print("Invalid email or password.")
    logger.error(f"Invalid email or password: {email}")


def success_create_collaborator_view(collaborator):
    print("Collaborator successfully created")
    logger.info("Collaborator successfully created: \n"
                f"{collaborator}")


def validation_error_view(e):
    print("Validation error:", e)
    logger.error(e)


def list_collaborators_view(collaborators):
    for collaborator in collaborators:
        print(collaborator)


def success_delete_collaborator_view(collaborator_infos):
    print("Collaborator successfully deleted")
    logger.info(f"Collaborator successfully deleted: {collaborator_infos}")


def error_collaborator_not_found_view(**kargs):
    print("Collaborator doesn't exist")
    logger.error(f"Collaborator doesn't exist: {kargs}")


def success_update_collaborator_view(collaborator):
    print("Collaborator updated")
    logger.info(f"Collaborator updated: {collaborator}")


def display_user_infos(user):
    print(f"{user.name}: id={user.id}, email={user.email}, role={user.role_id}")
