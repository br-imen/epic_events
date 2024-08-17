from datetime import datetime
from unittest.mock import patch
from controllers.event_controller import (
    create_event_controller,
    update_event_controller,
    delete_event_controller,
    list_events_controller,
)
from models.event import Event
from sqlalchemy.orm import Session


def test_create_event_controller(
    test_db: Session, client, collaborator, contract, capsys
):
    contract_id = contract.id
    with patch("controllers.event_controller.SessionLocal", return_value=test_db):
        create_event_controller(
            contract_id=contract_id,
            description="Test Event",
            date_start="2024-08-15 10:00:00",
            date_end="2024-08-15 12:00:00",
            location="Conference Room",
            attendees=20,
            notes="Important meeting.",
        )

    # Check the output printed by the view
    captured = capsys.readouterr()
    assert "event created" in captured.out

    # Verify the event was saved to the database
    event = test_db.query(Event).filter_by(contract_id=contract_id).first()
    assert event is not None
    assert event.description == "Test Event"
    assert event.location == "Conference Room"


def test_update_event_controller(
    test_db: Session, client, collaborator, contract, capsys
):
    client_id = client.id
    contract_id = contract.id
    with patch("controllers.event_controller.SessionLocal", return_value=test_db):
        event = Event(
            client_id=client_id,
            contract_id=contract.id,
            description="Initial Event",
            date_start=datetime(2024, 8, 15, 10, 0, 0),
            date_end=datetime(2024, 8, 15, 12, 0, 0),
            collaborator_support_id=collaborator.id,
            location="Conference Room A",
            attendees=15,
            notes="Initial notes.",
        )
        event.save(test_db)
        event_id = event.id
        update_event_controller(
            id=event_id,
            contract_id=contract_id,
            description="Updated Event",
            date_start=datetime(2024, 8, 16, 10, 0, 0),
            date_end=datetime(2024, 8, 16, 12, 0, 0),
            collaborator_support_id=collaborator.id,
            location="Conference Room B",
            attendees=30,
            notes="Updated notes.",
        )

    # Check the output printed by the view
    captured = capsys.readouterr()
    assert "event updated" in captured.out

    # Verify the event was updated in the database
    updated_event = test_db.query(Event).filter_by(id=event_id).first()
    assert updated_event.description == "Updated Event"
    assert updated_event.location == "Conference Room B"
    assert updated_event.attendees == 30


def test_delete_event_controller(
    test_db: Session, client, collaborator, contract, capsys
):
    with patch("controllers.event_controller.SessionLocal", return_value=test_db):
        event = Event(
            client_id=client.id,
            contract_id=contract.id,
            description="Event to Delete",
            date_start=datetime(2024, 8, 15, 10, 0, 0),
            date_end=datetime(2024, 8, 15, 12, 0, 0),
            collaborator_support_id=collaborator.id,
            location="Conference Room",
            attendees=10,
            notes="To be deleted.",
        )
        event.save(test_db)

        delete_event_controller(id=event.id)

    # Check the output printed by the view
    captured = capsys.readouterr()
    assert "event deleted" in captured.out

    # Verify the event was deleted from the database
    deleted_event = test_db.query(Event).filter_by(id=event.id).first()
    assert deleted_event is None


def test_list_events_controller(
    test_db: Session, client, collaborator, contract, capsys
):
    with patch(
        "controllers.event_controller.SessionLocal", return_value=test_db
    ), patch(
        "controllers.event_controller.get_login_collaborator",
        return_value=collaborator,
    ):

        event1 = Event(
            client_id=client.id,
            contract_id=contract.id,
            description="First Event",
            date_start=datetime(2024, 8, 15, 10, 0, 0),
            date_end=datetime(2024, 8, 15, 12, 0, 0),
            collaborator_support_id=collaborator.id,
            location="Conference Room A",
            attendees=25,
            notes="First event notes.",
        )
        event2 = Event(
            client_id=client.id,
            contract_id=contract.id,
            description="Second Event",
            date_start=datetime(2024, 8, 16, 10, 0, 0),
            date_end=datetime(2024, 8, 16, 12, 0, 0),
            collaborator_support_id=collaborator.id,
            location="Conference Room B",
            attendees=40,
            notes="Second event notes.",
        )
        test_db.add(event1)
        test_db.add(event2)
        test_db.commit()

        list_events_controller(filters={})

    # Check the output printed by the view
    captured = capsys.readouterr()
    assert "First Event" in captured.out
    assert "Second Event" in captured.out
