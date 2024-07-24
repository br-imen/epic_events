from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base



class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    company_name = Column(String)
    creation_date = Column(DateTime, default=datetime.utcnow)
    last_contact = Column(DateTime, default=datetime.utcnow)
    commercial_collaborator_id = Column(Integer, ForeignKey('collaborators.id'))

    # Define a relationship to the Commercial model
    collaborator = relationship("Collaborator", back_populates="clients")
    contracts = relationship("Contract", order_by="Contract.id", back_populates="client")
    events = relationship("Event", order_by="Event.id", back_populates="client")


    # Active Record CRUD Methods
    def save(self, session):
        session.add(self)
        session.commit()

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.last_contact = datetime.utcnow()  # Update the last_contact time
        session.merge(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    @staticmethod
    def get_by_id(client_id, session):
        return session.query(Client).filter(Client.id == client_id).first()

    @staticmethod
    def get_all(session):
        return session.query(Client).all()

    def __str__(self):
        return (
            f"Client {self.id}: {self.full_name}, Email: {self.email}, Phone: {self.phone_number}, "
            f"Company: {self.company_name}, Created: {self.creation_date}, "
            f"Last Contact: {self.last_contact}, Commercial id: {self.commercial_collaborator_id}"
        )
