from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional


class EventInput(BaseModel):
    client_id: int
    contract_id: int
    description: str
    date_start: datetime
    date_end: datetime
    support_contact_name: str
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
    support_contact_name: Optional[str] = None
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
