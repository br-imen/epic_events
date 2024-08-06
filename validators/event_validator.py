from datetime import datetime
from pydantic import BaseModel, ValidationError, validator
from typing import Optional

from views.event_view import validation_error_event_view


class EventInput(BaseModel):
    client_id: int
    contract_id: int
    description: str
    date_start: datetime
    date_end: datetime
    collaborator_support_id: Optional[int] = None
    location: str
    attendees: int
    notes: Optional[str] = None

    @validator("date_end")
    def check_date(cls, date_end, values):
        if "date_start" in values and date_end <= values["date_start"]:
            raise ValueError("End date must be after start date.")
        return date_end

    @validator("attendees")
    def check_attendees(cls, attendees):
        if attendees < 0:
            raise ValueError("Attendees must be a non-negative integer.")
        return attendees


class EventInputUpdate(BaseModel):
    id: int
    client_id: Optional[int] = None
    contract_id: Optional[int] = None
    description: Optional[str] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    collaborator_support_id: Optional[int] = None
    location: Optional[str] = None
    attendees: Optional[int] = None
    notes: Optional[str] = None

    @validator("date_end")
    def check_date(cls, date_end, values):
        if (
            "date_start" in values
            and date_end
            and values["date_start"]
            and date_end <= values["date_start"]
        ):
            raise ValueError("End date must be after start date.")
        return date_end

    @validator("attendees")
    def check_attendees(cls, attendees):
        if attendees is not None and attendees < 0:
            raise ValueError("Attendees must be a non-negative integer.")
        return attendees


class EventDeleteInput(BaseModel):
    id: int


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
