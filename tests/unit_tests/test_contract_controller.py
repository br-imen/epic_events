from unittest.mock import MagicMock, patch
from controllers.contract_controller import (
    create_contract_controller,
    list_contracts_controller,
    delete_contract_controller,
    update_contract_controller,
)

def test_create_contract_controller(mock_session):
    with patch("controllers.contract_controller.SessionLocal", return_value=mock_session), \
        patch("controllers.contract_controller.validate_create_contract_input", return_value=MagicMock(dict=lambda: {})), \
        patch("controllers.contract_controller.Contract") as mock_contract, \
        patch("controllers.contract_controller.success_create_contract_view") as mock_success_view:

        create_contract_controller(1, 2, 1000, 500, "Active")
        mock_contract.assert_called_once_with(
            client_id=1,
            commercial_collaborator_id=2,
            total_amount=1000,
            amount_due=500,
            status="Active"
        )
        mock_contract.return_value.save.assert_called_once_with(mock_session)
        mock_success_view.assert_called_once()

def test_create_contract_controller_invalid_input(mock_session):
    with patch("controllers.contract_controller.SessionLocal", return_value=mock_session), \
        patch("controllers.contract_controller.validate_create_contract_input", return_value=None), \
        patch("controllers.contract_controller.Contract") as mock_contract, \
        patch("controllers.contract_controller.success_create_contract_view") as mock_success_view:

        create_contract_controller(1, 2, 1000, 500, "Active")
        mock_contract.assert_not_called()
        mock_success_view.assert_not_called()

def test_list_contracts_controller(mock_session):
    with patch("controllers.contract_controller.SessionLocal", return_value=mock_session), \
        patch("controllers.contract_controller.Contract.get_all") as mock_get_all, \
        patch("controllers.contract_controller.list_contracts_view") as mock_list_view:

        mock_contracts = [MagicMock(id=1), MagicMock(id=2)]
        mock_get_all.return_value = mock_contracts

        list_contracts_controller(filters=[])
        mock_get_all.assert_called_once_with(mock_session, [])
        mock_list_view.assert_called_once_with(mock_contracts)

def test_delete_contract_controller(mock_session):
    with patch("controllers.contract_controller.SessionLocal", return_value=mock_session), \
        patch("controllers.contract_controller.Contract.get_by_id", return_value=MagicMock(id=1)) as mock_get_by_id, \
        patch("controllers.contract_controller.success_delete_contract_view") as mock_success_view:

        delete_contract_controller(1)
        mock_get_by_id.assert_called_once_with(1, mock_session)
        mock_get_by_id.return_value.delete.assert_called_once_with(mock_session)
        mock_success_view.assert_called_once()

def test_delete_contract_controller_contract_not_found(mock_session):
    with patch("controllers.contract_controller.SessionLocal", return_value=mock_session), \
        patch("controllers.contract_controller.Contract.get_by_id", return_value=None) as mock_get_by_id, \
        patch("controllers.contract_controller.success_delete_contract_view") as mock_success_view, \
        patch("controllers.contract_controller.error_contract_not_found_view") as mock_error_view:

        delete_contract_controller(1)
        mock_get_by_id.assert_called_once_with(1, mock_session)
        mock_success_view.assert_not_called()
        mock_error_view.assert_called_once()

def test_update_contract_controller(mock_session):
    with patch("controllers.contract_controller.SessionLocal", return_value=mock_session), \
        patch("controllers.contract_controller.validate_update_contract_input", return_value=MagicMock(dict=lambda: {})), \
        patch("controllers.contract_controller.Contract.get_by_id", return_value=MagicMock(id=1)) as mock_get_by_id, \
        patch("controllers.contract_controller.Client.get_by_id", return_value=MagicMock(id=2)) as mock_get_client_by_id, \
        patch("controllers.contract_controller.Collaborator.get_by_id", return_value=MagicMock(id=3)) as mock_get_collaborator_by_id, \
        patch("controllers.contract_controller.success_update_contract_view") as mock_success_view, \
        patch("controllers.contract_controller.error_contract_not_found_view") as mock_error_contract_view, \
        patch("controllers.contract_controller.error_client_collaborator_not_found_view") as mock_error_client_collaborator_view:

        update_contract_controller(1, 2, 3, 1000, 500, "Active")
        mock_get_by_id.assert_called_once_with(1, session=mock_session)
        mock_get_client_by_id.assert_called_once_with(2, mock_session)
        mock_get_collaborator_by_id.assert_called_once_with(3, mock_session)
        mock_success_view.assert_called_once()
        mock_error_contract_view.assert_not_called()
        mock_error_client_collaborator_view.assert_not_called()

def test_update_contract_controller_contract_not_found(mock_session):
    with patch("controllers.contract_controller.SessionLocal", return_value=mock_session), \
        patch("controllers.contract_controller.validate_update_contract_input", return_value=MagicMock(dict=lambda: {})), \
        patch("controllers.contract_controller.Contract.get_by_id", return_value=None) as mock_get_by_id, \
        patch("controllers.contract_controller.error_contract_not_found_view") as mock_error_contract_view, \
        patch("controllers.contract_controller.error_client_collaborator_not_found_view") as mock_error_client_collaborator_view:

        update_contract_controller(1, 2, 3, 1000, 500, "Active")
        mock_get_by_id.assert_called_once_with(1, session=mock_session)
        mock_error_contract_view.assert_called_once()
        mock_error_client_collaborator_view.assert_not_called()

def test_update_contract_controller_client_not_found(mock_session):
    with patch("controllers.contract_controller.SessionLocal", return_value=mock_session), \
        patch("controllers.contract_controller.validate_update_contract_input", return_value=MagicMock(dict=lambda: {})), \
        patch("controllers.contract_controller.Contract.get_by_id", return_value=MagicMock(id=1)) as mock_get_by_id, \
        patch("controllers.contract_controller.Client.get_by_id", return_value=None) as mock_get_client_by_id, \
        patch("controllers.contract_controller.error_contract_not_found_view") as mock_error_contract_view, \
        patch("controllers.contract_controller.error_client_collaborator_not_found_view") as mock_error_client_collaborator_view:

        update_contract_controller(1, 2, 3, 1000, 500, "Active")
        mock_get_by_id.assert_called_once_with(1, session=mock_session)
        mock_get_client_by_id.assert_called_once_with(2, mock_session)
        mock_error_contract_view.assert_not_called()
        mock_error_client_collaborator_view.assert_called_once()

def test_update_contract_controller_collaborator_not_found(mock_session):
    with patch("controllers.contract_controller.SessionLocal", return_value=mock_session), \
        patch("controllers.contract_controller.validate_update_contract_input", return_value=MagicMock(dict=lambda: {})), \
        patch("controllers.contract_controller.Contract.get_by_id", return_value=MagicMock(id=1)) as mock_get_by_id, \
        patch("controllers.contract_controller.Client.get_by_id", return_value=MagicMock(id=2)) as mock_get_client_by_id, \
        patch("controllers.contract_controller.Collaborator.get_by_id", return_value=None) as mock_get_collaborator_by_id, \
        patch("controllers.contract_controller.error_contract_not_found_view") as mock_error_contract_view, \
        patch("controllers.contract_controller.error_client_collaborator_not_found_view") as mock_error_client_collaborator_view:

        update_contract_controller(1, 2, 3, 1000, 500, "Active")
        mock_get_by_id.assert_called_once_with(1, session=mock_session)
        mock_get_client_by_id.assert_called_once_with(2, mock_session)
        mock_get_collaborator_by_id.assert_called_once_with(3, mock_session)
        mock_error_contract_view.assert_not_called()
        mock_error_client_collaborator_view.assert_called_once()