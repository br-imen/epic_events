from config.auth import get_login_collaborator
from models import Collaborator
from config.database import SessionLocal
from validators.event_validator import validate_create_event, validate_delete_event_input, validate_update_event
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
    session = SessionLocal()
    client_id = Contract.get_by_id(contract_id, session).client_id if contract_id else None
    event_data = {
        "client_id": client_id,
        "contract_id": contract_id,
        "description": description,
        "date_start": date_start,
        "date_end": date_end,
        "collaborator_support_id": collaborator_support_id ,
        "location": location,
        "attendees": attendees,
        "notes": notes,
    }
    validated_data = validate_create_event(**event_data)
    if validated_data:
        session = SessionLocal()
        try:
            found_support = Collaborator.get_by_id(collaborator_support_id , session)
            found_contract = Contract.get_by_id(contract_id,session)
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
    session = SessionLocal()
    # client = Contract.get_by_id(contract_id, session)
    client_id = Contract.get_by_id(contract_id, session).client_id if contract_id else None
    event_data = {
        "id": id,
        "client_id": client_id,
        "contract_id": contract_id,
        "description": description,
        "date_start": date_start,
        "date_end": date_end,
        "collaborator_support_id": collaborator_support_id ,
        "location": location,
        "attendees": attendees,
        "notes": notes,
    }
    validated_data = validate_update_event(**event_data)
    if validated_data:
        session = SessionLocal()
        try:
            event = Event.get_by_id(id, session)
            if event:
                if client_id and contract_id:
                    collaborator = Collaborator.get_by_id(
                        collaborator_support_id , session=session
                    )
                    client = Client.get_by_id(client_id, session)
                    contract = Contract.get_by_id(contract_id,session)
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
    session = SessionLocal()
    login_collaborator = get_login_collaborator(session) 
    try:
        events = Event.get_all(session, filters, login_collaborator)
        return list_event_view(events)
    finally:
        session.close()
