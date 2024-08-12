from unittest.mock import patch
import pytest
from controllers.collaborator_controller import (
    create_collaborator_controller,
    update_collaborator_controller,
    delete_collaborator_controller,
    list_collaborators_controller,
    authentication,
)
from models.collaborator import Collaborator


# Integration test for creating a collaborator
def test_create_collaborator_controller(test_db, capsys):
    # Create a collaborator
    with patch('controllers.collaborator_controller.SessionLocal', return_value=test_db):
        create_collaborator_controller(
            employee_number=5432,
            name="Test User",
            email="testcollaborator@example.com",
            role_id=1,
            password="securepassword"
        )

    # Check the output printed by the view
    captured = capsys.readouterr()
    assert "Collaborator successfully created" in captured.out

    # Verify the collaborator was saved to the database
    collaborator = test_db.query(Collaborator).filter_by(email="testcollaborator@example.com").first()
    assert collaborator is not None
    assert collaborator.name == "Test User"

    # Clean up: delete the collaborator to avoid integrity errors in other tests
    collaborator.delete(test_db)
    test_db.commit()


# Integration test for updating a collaborator
def test_update_collaborator_controller(test_db, capsys):
    # Create a collaborator to update
    collaborator = Collaborator(
        employee_number=5432,
        name="Old Name",
        email="testcollaborator@example.com",
        role_id=1,
        password="securepassword"
    )
    collaborator.save(test_db)
    with patch('controllers.collaborator_controller.SessionLocal', return_value=test_db):
        update_collaborator_controller(
            employee_number=5432,
            name="Updated Name",
            email="updated@example.com",
            role_id=1,
            password="newpassword"
        )

    # Check the output printed by the view
    captured = capsys.readouterr()
    assert "Collaborator updated" in captured.out

    # Verify the collaborator was updated in the database
    updated_collaborator = test_db.query(Collaborator).filter_by(email="updated@example.com").first()
    assert updated_collaborator.name == "Updated Name"
    assert updated_collaborator.verify_password("newpassword")


# Integration test for deleting a collaborator
def test_delete_collaborator_controller(test_db, capsys):
    # Create a collaborator to delete
    collaborator = Collaborator(
        employee_number=123,
        name="Test User",
        email="testuser@example.com",
        role_id=1,
        password="securepassword"
    )
    collaborator.save(test_db)
    with patch('controllers.collaborator_controller.SessionLocal', return_value=test_db):
        delete_collaborator_controller(employee_number=123)

    # Check the output printed by the view
    captured = capsys.readouterr()
    assert "Collaborator successfully deleted" in captured.out

    # Verify the collaborator was deleted from the database
    deleted_collaborator = test_db.query(Collaborator).filter_by(email="testuser@example.com").first()
    assert deleted_collaborator is None


# Integration test for listing collaborators
def test_list_collaborators_controller(test_db, capsys):
    # Create some collaborators to list
    collaborator1 = Collaborator(
        employee_number=123,
        name="Test User 1",
        email="testuser1@example.com",
        role_id=1,
        password="securepassword"
    )
    collaborator2 = Collaborator(
        employee_number=124,
        name="Test User 2",
        email="testuser2@example.com",
        role_id=1,
        password="securepassword"
    )
    collaborator1.save(test_db)
    collaborator2.save(test_db)
    with patch('controllers.collaborator_controller.SessionLocal', return_value=test_db):
        list_collaborators_controller()

    # Check the output printed by the view
    captured = capsys.readouterr()
    assert "Test User 1" in captured.out
    assert "Test User 2" in captured.out


# Integration test for authentication
def test_authentication(test_db, capsys):
    # Create a collaborator to authenticate
    collaborator = Collaborator(
        employee_number=123,
        name="Test User",
        email="testuser@example.com",
        role_id=1,
        password="securepassword"
    )
    collaborator.save(test_db)
    with patch('controllers.collaborator_controller.SessionLocal', return_value=test_db):
        result = authentication(email="testuser@example.com", password="securepassword")

    # Check the output printed by the view
    captured = capsys.readouterr()
    assert "Login successful" in captured.out

    # Verify the authentication result
    assert result is not None
    assert "access_token" in result
    assert result["token_type"] == "bearer"
