from datetime import datetime
from pydantic import BaseModel, ValidationError, validator
from typing import Optional

from views.event_view import validation_error_event_view


class EventInput(BaseModel):
    """
    Represents the input data for an event.
    """

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
    """
    Represents the input data for updating an event.
    """

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
        """
        Check if the end date is valid based on the start date.

        Args:
            date_end (datetime): The end date of the event.
            values (dict): A dictionary containing the values of the event.

        Raises:
            ValueError: If the end date is before or equal to the start date.

        Returns:
            datetime: The validated end date.
        """
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
        """
        Check if the number of attendees is valid.

        Args:
            attendees (int): The number of attendees.

        Returns:
            int: The number of attendees if it is valid.

        Raises:
            ValueError: If the number of attendees is a negative integer.

        """
        if attendees is not None and attendees < 0:
            raise ValueError("Attendees must be a non-negative integer.")
        return attendees


class EventDeleteInput(BaseModel):
    """
    Represents the input data for deleting an event.

    Attributes:
        id (int): The ID of the event to be deleted.
    """
    id: int


def validate_create_event(**kwargs):
    """
    Validates the input for creating an event.

    Args:
        **kwargs: Keyword arguments representing the event input.

    Returns:
        EventInput: The validated event input.

    Raises:
        ValidationError: If the input is invalid.
    """
    try:
        user_input = EventInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_event_view(e)


def validate_delete_event_input(**kwargs):
    """
    Validates the input for deleting an event.

    Args:
        **kwargs: Keyword arguments representing the input
        parameters for deleting an event.

    Returns:
        EventDeleteInput: The validated input for deleting an event.

    Raises:
        ValidationError: If the input is invalid.
    """
    try:
        user_input = EventDeleteInput(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_event_view(e)


def validate_update_event(**kwargs):
    """
    Validates the input for updating an event.

    Args:
        **kwargs: Keyword arguments representing the event input.

    Returns:
        EventInputUpdate: The validated event input.

    Raises:
        ValidationError: If the input is invalid.
    """
    try:
        user_input = EventInputUpdate(**kwargs)
        return user_input
    except ValidationError as e:
        validation_error_event_view(e)
