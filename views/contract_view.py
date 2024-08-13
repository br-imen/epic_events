import logging


def validation_error_contract_view(e):
    print(e)
    logging.error(e)


def success_create_contract_view():
    print("Contract successfully created")


def list_contracts_view(contracts):
    for contract in contracts:
        print(contract)


def error_client_collaborator_not_found_view():
    print("client or collaborator not found")
    logging.error("client or collaborator not found")


def success_delete_contract_view():
    print("Contract deleted")


def error_contract_not_found_view():
    print("Contract not found")
    logging.error("Contract not found")


def success_update_contract_view():
    print("Contract updated")


def success_signed_contract_view():
    logging.info("Contract signed")
