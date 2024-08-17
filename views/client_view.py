from config.logger import get_logger


logger = get_logger()


def validation_error_client_view(e):
    print(e)
    logger.error(e)


def success_create_client_view():
    print("client created")


def list_client_view(clients):
    for client in clients:
        print(client)


def success_delete_client_view():
    print("Client deleted")


def error_client_not_found_view(client_id):
    print("Client not found")
    logger.error(f"Client not found: {client_id}")


def error_commercial_not_found_view(id):
    print("commercial not found")
    logger.error(f"commercial not found : {id}")


def success_update_client_view():
    print("CLient updated")
