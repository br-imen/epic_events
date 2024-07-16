from pydantic import ValidationError
from config.database import SessionLocal
from controllers.contract_validator import ContractDeleteInput, ContractInput
from models.client import Client
from models.collaborator import Collaborator
from models.contract import Contract
from views.contract_view import error_client_collaborator_not_found_view, error_contract_not_found_view, list_contracts_view, success_create_contract_view, success_delete_contract_view, validation_error_contract_view


def validate_create_contract_input(**kwargs):
    try:
        user_input = ContractInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_contract_view(e)


def validate_delete_contract_input(**kwargs):
    try:
        user_input = ContractDeleteInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_contract_view(e)  


def create_contract_controller(client_id, commercial_contact, total_amount, amount_due, status):
    
    contract_data = {
        "client_id": client_id,
        "commercial_contact": commercial_contact,
        "total_amount": total_amount,
        "amount_due": amount_due,
        "status": status
    }
    validate_data = validate_create_contract_input(**contract_data)
    if validate_data:
        session = SessionLocal()
        try:
            find_commercial = Collaborator.get_by_name(commercial_contact,session)
            find_client = Client.get_by_id(client_id,session)
            if find_client and find_commercial:
                contract = Contract(**contract_data)
                contract.save(session)
                success_create_contract_view()
            else:
                error_client_collaborator_not_found_view()
        finally:
            session.close()


def list_contracts_controller():
    session = SessionLocal()
    try:
        contracts = Contract.get_all(session)
        return list_contracts_view(contracts)
    finally:
        session.close()


def delete_contract_controller(contract_id):
    data = {"id": contract_id }
    validated_data = validate_delete_contract_input(**data)
    if validated_data:
        session = SessionLocal()
        try:
            contract = Contract.get_by_id(contract_id, session)
            if contract:
                contract.delete(session)
                success_delete_contract_view()
            else:
                error_contract_not_found_view()
        finally:
            session.close()
 