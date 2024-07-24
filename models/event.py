from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from models.client import Client
from models.collaborator import Collaborator


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    description = Column(String, nullable=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    collaborator_support_id = Column(Integer, ForeignKey('collaborators.id'))
    location = Column(String, nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)

    client = relationship("Client", back_populates="events")
    contract = relationship("Contract", back_populates="events")
    collaborator_support = relationship("Collaborator", back_populates="events")

    def save(self, session):
        session.add(self)
        session.commit()

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.merge(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    @staticmethod
    def get_all(session):
        return session.query(Event).all()
    
    @staticmethod
    def get_by_id(event_id,session):
        return session.query(Event).filter(Event.id == event_id).first()

    def __str__(self):
        return (
            f"Event {self.id} Details:\n"
            f"Client ID: {self.client_id}\n"
            f"Contract ID: {self.contract_id}\n"
            f"Description: {self.description}\n"
            f"Start Date: {self.date_start.strftime('%d-%m-%Y %I:%M %p')}\n"
            f"End Date: {self.date_end.strftime('%d-%m-%Y %I:%M %p')}\n"
            f"Collaborator support id : {self.collaborator_support_id}\n"
            f"Location: {self.location}\n"
            f"Attendees: {self.attendees}\n"
            f"Notes: {self.notes if self.notes else 'None'}"
            )