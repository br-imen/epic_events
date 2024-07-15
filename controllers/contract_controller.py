from pydantic import ValidationError
from config.database import SessionLocal
from controllers.contract_validator import ContractInput
from models.contract import Contract
from views.contract_view import success_create_contract_view, validation_error_contract_view


def validate_create_contract_input(**kwargs):
    try:
        user_input = ContractInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_contract_view(e)


def create_contract_controller(client_id, commercial_contact, total_amount, amount_due, status):
    try:
        contract_data = {
            "client_id": client_id,
            "commercial_contact": commercial_contact,
            "total_amount": total_amount,
            "amount_due": amount_due,
            "status": status
        }
        session = SessionLocal()
        contract = Contract(**contract_data)
        contract.save(session)
        success_create_contract_view()
    finally:
        session.close()


def list_contracts_controller():
    session = SessionLocal()
    try:
        contracts = Contract.get_all(session)
        return list_contract_view(contracts)
    finally:
        session.close()

