from unittest.mock import patch
from controllers.contract_controller import (
    create_contract_controller,
    list_contracts_controller,
    delete_contract_controller,
    update_contract_controller,
)
from models.contract import Contract
from sqlalchemy.orm import Session


def test_create_contract_controller(test_db: Session, client, collaborator, capsys):
    client_id = client.id
    with patch("controllers.contract_controller.SessionLocal", return_value=test_db):
        create_contract_controller(
            client_id=client.id,
            commercial_collaborator_id=collaborator.id,
            total_amount=10000.00,
            amount_due=5000.00,
            status=True,
        )

    # Check the output printed by the view
    captured = capsys.readouterr()
    assert "Contract successfully created" in captured.out

    # Verify the contract was saved to the database
    contract = test_db.query(Contract).filter_by(client_id=client_id).first()
    assert contract is not None
    assert contract.total_amount == 10000.00
    assert contract.amount_due == 5000.00


def test_list_contracts_controller(test_db: Session, client, collaborator, capsys):
    # Create some contracts to list
    contract1 = Contract(
        client_id=client.id,
        commercial_collaborator_id=collaborator.id,
        total_amount=15000.00,
        amount_due=7000.00,
        status=True,
    )
    contract2 = Contract(
        client_id=client.id,
        commercial_collaborator_id=collaborator.id,
        total_amount=12000.00,
        amount_due=0.00,
        status=False,
    )
    test_db.add(contract1)
    test_db.add(contract2)
    test_db.commit()
    with patch("controllers.contract_controller.SessionLocal", return_value=test_db):
        list_contracts_controller(filters={})

    # Check the output printed by the view
    captured = capsys.readouterr()
    assert "Contract id" in captured.out
    assert "total_amount=15000.00" in captured.out
    assert "total_amount=12000.00" in captured.out


def test_delete_contract_controller(test_db: Session, client, collaborator, capsys):
    # Create a contract to delete
    contract = Contract(
        client_id=client.id,
        commercial_collaborator_id=collaborator.id,
        total_amount=20000.00,
        amount_due=10000.00,
        status=True,
    )
    contract.save(test_db)
    with patch("controllers.contract_controller.SessionLocal", return_value=test_db):
        delete_contract_controller(contract_id=contract.id)

    # Check the output printed by the view
    captured = capsys.readouterr()
    assert "Contract deleted" in captured.out

    # Verify the contract was deleted from the database
    deleted_contract = test_db.query(Contract).filter_by(id=contract.id).first()
    assert deleted_contract is None


def test_update_contract_controller(test_db: Session, client, collaborator, capsys):
    # Create a contract to update
    contract = Contract(
        client_id=client.id,
        commercial_collaborator_id=collaborator.id,
        total_amount=25000.00,
        amount_due=15000.00,
        status=True,
    )
    contract.save(test_db)
    contract_id = contract.id
    with patch("controllers.contract_controller.SessionLocal", return_value=test_db):
        update_contract_controller(
            id=contract.id,
            client_id=client.id,
            commercial_collaborator_id=collaborator.id,
            total_amount=25000.00,
            amount_due=10000.00,
            status=False,
        )

    # Check the output printed by the view
    captured = capsys.readouterr()
    assert "Contract updated" in captured.out

    # Verify the contract was updated in the database
    updated_contract = test_db.query(Contract).filter_by(id=contract_id).first()
    assert updated_contract.amount_due == 10000.00
    assert updated_contract.status is False
