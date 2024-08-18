from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class Event(Base):
    """
    Represents an event in the system.

    Attributes:
        id (int): The unique identifier of the event.
        client_id (int): The ID of the client associated with the event.
        contract_id (int): The ID of the contract associated with the event.
        description (str): The description of the event.
        date_start (datetime): The start date and time of the event.
        date_end (datetime): The end date and time of the event.
        collaborator_support_id (int): The ID of the collaborator
        providing support for the event.
        location (str): The location of the event.
        attendees (int): The number of attendees for the event.
        notes (str): Additional notes for the event.

    Relationships:
        client (Client): The client associated with the event.
        contract (Contract): The contract associated with the event.
        collaborator_support (Collaborator): The collaborator providing
        support for the event.
    """

    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer,
                       ForeignKey("clients.id", ondelete="CASCADE"),
                       nullable=False)
    contract_id = Column(Integer,
                         ForeignKey("contracts.id", ondelete="CASCADE"),
                         nullable=False)
    description = Column(String, nullable=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    collaborator_support_id = Column(
        Integer, ForeignKey("collaborators.id", ondelete="SET NULL"), nullable=True
    )
    location = Column(String, nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)

    client = relationship("Client", back_populates="events")
    contract = relationship("Contract", back_populates="event")
    collaborator_support = relationship("Collaborator", back_populates="events")

    def save(self, session):
        session.add(self)
        session.commit()

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)
        session.merge(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    @staticmethod
    def get_all(session, filters, login_collaborator):
        events = session.query(Event)
        if "with_no_support" in filters:
            events = events.filter(Event.collaborator_support_id.is_(None))
        if "assigned_to_me" in filters:
            events = events.filter(
                Event.collaborator_support_id == login_collaborator.id
            )
        return events.all()

    @staticmethod
    def get_by_id(event_id, session):
        return session.query(Event).filter(Event.id == event_id).first()

    def __str__(self):
        return (
            f"Event id={self.id}, Details= {self.description},"
            f"Client ID={self.client_id}, "
            f"Contract ID={self.contract_id}, "
            f"Description={self.description}, "
            f"Start Date={self.date_start.strftime('%d-%m-%Y %I:%M %p')}, "
            f"End Date={self.date_end.strftime('%d-%m-%Y %I:%M %p')}, "
            f"Collaborator support id={self.collaborator_support_id}, "
            f"Location={self.location}, "
            f"Attendees={self.attendees}, "
            f"Notes={self.notes if self.notes else 'None'} \n"
        )
