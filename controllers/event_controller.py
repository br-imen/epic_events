from pydantic import ValidationError
from models import event, Collaborator
from config.database import SessionLocal
from controllers.event_validator import EventDeleteInput, EventInput, EventInputUpdate
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
    validation_error_event_view,
)


def validate_create_event(**kwargs):
    try:
        user_input = EventInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_event_view(e)


def validate_delete_event_input(**kwargs):
    try:
        user_input = EventDeleteInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_event_view(e)


def validate_update_event(**kwargs):
    try:
        user_input = EventInputUpdate(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_event_view(e)


def create_event_controller(
    client_id,
    contract_id,
    description,
    date_start,
    date_end,
    support_contact_name,
    location,
    attendees,
    notes,
):
    event_data = {
        "client_id": client_id,
        "contract_id": contract_id,
        "description": description,
        "date_start": date_start,
        "date_end": date_end,
        "support_contact_name": support_contact_name,
        "location": location,
        "attendees": attendees,
        "notes": notes,
    }
    validated_data = validate_create_event(**event_data)
    if validated_data:
        session = SessionLocal()
        try:
            found_support = Collaborator.get_by_name(support_contact_name, session)
            found_contract = Contract.get_by_id(contract_id,session)
            found_client = Client.get_by_id(client_id,session)
            if found_support and found_contract and found_client:
                new_event = Event(**validated_data.dict())
                new_event.save(session)
                success_create_event_view()
            else:
                error_contact_client_support_not_found_view()
        finally:
            session.close()


def update_event_controller(
    id,
    client_id,
    contract_id,
    description,
    date_start,
    date_end,
    support_contact_name,
    location,
    attendees,
    notes,
):
    event_data = {
        "id": id,
        "client_id": client_id,
        "contract_id": contract_id,
        "description": description,
        "date_start": date_start,
        "date_end": date_end,
        "support_contact_name": support_contact_name,
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
                collaborator = Collaborator.get_by_name(
                    support_contact_name, session=session
                )
                client = Client.get_by_id(client_id, session)
                contract = Contract.get_by_id(contract_id,session)
                if collaborator and client and contract:
                    event.update(session, **validated_data.dict())
                    success_update_event_view()
                else:
                    error_contact_client_support_not_found_view()
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


def list_events_controller():
    session = SessionLocal()
    try:
        events = Event.get_all(session)
        return list_event_view(events)
    finally:
        session.close()
