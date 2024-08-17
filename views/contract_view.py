from config.logger import get_logger


logger = get_logger()


def validation_error_contract_view(e):
    print(e)
    logger.error(e)


def success_create_contract_view():
    print("Contract successfully created")


def list_contracts_view(contracts):
    for contract in contracts:
        print(contract)


def error_client_collaborator_not_found_view(**kwargs):
    print("client or collaborator not found")
    logger.error(f"client or collaborator not found: {kwargs}")


def success_delete_contract_view():
    print("Contract deleted")


def error_contract_not_found_view(contract_id):
    print("Contract not found")
    logger.error(f"Contract not found: {contract_id}")


def success_update_contract_view():
    print("Contract updated")


def success_signed_contract_view(contract):
    logger.info(f"Contract signed: {contract}")
