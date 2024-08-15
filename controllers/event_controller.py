from config.auth import get_login_collaborator
from models import Collaborator
from config.database import SessionLocal
from validators.event_validator import (
    validate_create_event,
    validate_delete_event_input,
    validate_update_event,
)
from models.client import Client
from models.contract import Contract
from models.event import Event
from views.event_view import (
    error_contact_client_support_not_found_view,
    error_event_not_found_view,
    list_event_view,
    success_create_event_view,
    success_delete_event_view,
    success_update_event_view,
)


def create_event_controller(
    contract_id,
    description,
    date_start,
    date_end,
    collaborator_support_id,
    location,
    attendees,
    notes,
):
    """
    Create a new event.

    Args:
        contract_id (int): The ID of the contract associated with the event.
        description (str): The description of the event.
        date_start (datetime): The start date and time of the event.
        date_end (datetime): The end date and time of the event.
        collaborator_support_id (int): The ID of the collaborator
        providing support for the event.
        location (str): The location of the event.
        attendees (list): The list of attendees for the event.
        notes (str): Additional notes for the event.

    Returns:
        None
    """
    session = SessionLocal()
    client_id = (
        Contract.get_by_id(contract_id, session).client_id if contract_id else None
    )
    event_data = {
        "client_id": client_id,
        "contract_id": contract_id,
        "description": description,
        "date_start": date_start,
        "date_end": date_end,
        "collaborator_support_id": collaborator_support_id,
        "location": location,
        "attendees": attendees,
        "notes": notes,
    }
    validated_data = validate_create_event(**event_data)
    if validated_data:
        try:
            found_support = Collaborator.get_by_id(collaborator_support_id, session)
            found_contract = Contract.get_by_id(contract_id, session)
            if found_support and found_contract:
                if found_contract.status:
                    new_event = Event(**validated_data.dict())
                    new_event.save(session)
                    success_create_event_view()
            else:
                error_contact_client_support_not_found_view()
        finally:
            session.close()


def update_event_controller(
    id,
    contract_id=None,
    description=None,
    date_start=None,
    date_end=None,
    collaborator_support_id=None,
    location=None,
    attendees=None,
    notes=None,
):
    """
    Update an event with the given parameters.

    Args:
        id (int): The ID of the event to be updated.
        contract_id (int, optional): The ID of the contract
        associated with the event.
        description (str, optional): The updated description of the event.
        date_start (datetime, optional): The updated start
        date and time of the event.
        date_end (datetime, optional): The updated end date and time of the event.
        collaborator_support_id (int, optional): The ID of the collaborator
        providing support for the event.
        location (str, optional): The updated location of the event.
        attendees (List[str], optional): The updated list of attendees for the event.
        notes (str, optional): The updated notes for the event.

    Returns:
        None
    """
    session = SessionLocal()
    # client = Contract.get_by_id(contract_id, session)
    client_id = (
        Contract.get_by_id(contract_id, session).client_id if contract_id else None
    )
    event_data = {
        "id": id,
        "client_id": client_id,
        "contract_id": contract_id,
        "description": description,
        "date_start": date_start,
        "date_end": date_end,
        "collaborator_support_id": collaborator_support_id,
        "location": location,
        "attendees": attendees,
        "notes": notes,
    }
    validated_data = validate_update_event(**event_data)
    if validated_data:
        try:
            event = Event.get_by_id(id, session)
            if event:
                if client_id and contract_id:
                    collaborator = Collaborator.get_by_id(
                        collaborator_support_id, session=session
                    )
                    client = Client.get_by_id(client_id, session)
                    contract = Contract.get_by_id(contract_id, session)
                    if collaborator and client and contract:
                        event.update(session, **validated_data.dict())
                        success_update_event_view()
                    else:
                        error_contact_client_support_not_found_view()
                else:
                    event.update(session, **validated_data.dict())
                    success_update_event_view()
            else:
                error_event_not_found_view()
        finally:
            session.close()


def delete_event_controller(id):
    """
    Deletes an event with the given ID.

    Args:
        id (int): The ID of the event to be deleted.

    Returns:
        None
    """
    data = {"id": id}
    validated_data = validate_delete_event_input(**data)
    if validated_data:
        try:
            session = SessionLocal()
            event = Event.get_by_id(id, session)
            if event:
                event.delete(session)
                success_delete_event_view()
            else:
                error_event_not_found_view()
        finally:
            session.close()


def list_events_controller(filters):
    """
    Retrieve a list of events based on the provided filters.

    Args:
        filters (dict): A dictionary containing filters to apply to the event list.

    Returns:
        list: A list of events that match the provided filters.
    """
    session = SessionLocal()
    login_collaborator = get_login_collaborator(session)
    try:
        events = Event.get_all(session, filters, login_collaborator)
        return list_event_view(events)
    finally:
        session.close()
