from config.database import SessionLocal
from validators.contract_validator import (
    validate_create_contract_input,
    validate_delete_contract_input,
    validate_update_contract_input,
)
from models.client import Client
from models.contract import Contract
from views.contract_view import (
    error_client_collaborator_not_found_view,
    error_contract_not_found_view,
    list_contracts_view,
    success_create_contract_view,
    success_delete_contract_view,
    success_signed_contract_view,
    success_update_contract_view,
)


def create_contract_controller(
    client_id, total_amount, amount_due, status
):
    """
    Create a new contract.

    Args:
        client_id (int): The ID of the client.
        total_amount (float): The total amount of the contract.
        amount_due (float): The amount due for the contract.
        status (str): The status of the contract.

    Returns:
        None
    """
    contract_data = {
        "client_id": client_id,
        "total_amount": total_amount,
        "amount_due": amount_due,
        "status": status,
    }
    validate_data = validate_create_contract_input(**contract_data)
    if validate_data:
        session = SessionLocal()
        try:
            client = Client.get_by_id(client_id, SessionLocal())
            contract_data["commercial_collaborator_id"] = \
                client.commercial_collaborator_id
            contract = Contract(**contract_data)
            contract.save(session)
            success_create_contract_view()
        finally:
            session.close()


def list_contracts_controller(filters):
    """
    Retrieve a list of contracts based on the provided filters.

    Args:
        filters (dict): A dictionary containing filters to apply to the query.

    Returns:
        list: A list of contracts matching the provided filters.
    """
    session = SessionLocal()
    try:
        contracts = Contract.get_all(session, filters)
        return list_contracts_view(contracts)
    finally:
        session.close()


def delete_contract_controller(contract_id):
    """
    Deletes a contract based on the given contract ID.

    Args:
        contract_id (int): The ID of the contract to be deleted.

    Returns:
        None
    """
    data = {"id": contract_id}
    validated_data = validate_delete_contract_input(**data)
    if validated_data:
        session = SessionLocal()
        try:
            contract = Contract.get_by_id(contract_id, session)
            if contract:
                contract.delete(session)
                success_delete_contract_view()
            else:
                error_contract_not_found_view(contract_id)
        finally:
            session.close()


def update_contract_controller(
    id, client_id, total_amount, amount_due, status
):
    """
    Update a contract with the provided data.

    Args:
        id (int): The ID of the contract to be updated.
        client_id (int): The ID of the client associated with the contract.
        associated with the contract.
        total_amount (float): The total amount of the contract.
        amount_due (float): The amount due for the contract.
        status (bool): The status of the contract.

    Returns:
        None
    """
    contract_data = {
        "id": id,
        "client_id": client_id,
        "total_amount": total_amount,
        "amount_due": amount_due,
        "status": status,
    }
    validated_data = validate_update_contract_input(**contract_data)
    if validated_data:
        session = SessionLocal()
        try:
            contract = Contract.get_by_id(id, session=session)
            if contract:
                found_client = Client.get_by_id(client_id, session)
                try:
                    found_commercial_id = found_client.commercial_collaborator_id
                    data = validated_data.dict()
                    data["commercial_collaborator_id"] = found_commercial_id
                    contract.update(session, **validated_data.dict())
                    success_update_contract_view()
                    if contract_data["status"] is True:
                        success_signed_contract_view(contract)
                except AttributeError:
                    error_client_collaborator_not_found_view(
                        client_id=client_id,
                        )
            else:
                error_contract_not_found_view(id)
        finally:
            session.close()
