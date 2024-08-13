import logging


def validation_error_client_view(e):
    print(e)
    logging.error(e)


def success_create_client_view():
    print("client created")


def list_client_view(clients):
    for client in clients:
        print(client)


def success_delete_client_view():
    print("Client deleted")


def error_client_not_found_view():
    print("Client not found")
    logging.error("Client not found")


def error_commercial_not_found_view():
    print("commercial not found")
    logging.error("commercial not found")


def success_update_client_view():
    print("CLient updated")
