from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base


class Client(Base):
    """
    Represents a client in the system.

    Attributes:
        id (int): The primary key for the client.
        full_name (str): The full name of the client.
        email (str): The email address of the client.
        phone_number (str): The phone number of the client.
        company_name (str): The company name associated with the client.
        creation_date (datetime): The date when the client record was created.
        last_contact (datetime): The date when the client was last contacted.
        commercial_collaborator_id (int): Foreign key referencing
        the collaborator responsible for this client.
        collaborator (Collaborator): The collaborator associated with the client.
        contracts (list of Contract): A list of contracts associated
        with the client.
        events (list of Event): A list of events associated with the client.
    """

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    company_name = Column(String)
    creation_date = Column(DateTime, default=datetime.utcnow)
    last_contact = Column(DateTime, default=datetime.utcnow)
    commercial_collaborator_id = Column(Integer, ForeignKey("collaborators.id"))

    # Define a relationship to the Commercial model
    collaborator = relationship("Collaborator", back_populates="clients")
    contracts = relationship(
        "Contract", order_by="Contract.id", back_populates="client"
    )
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
            f"Client id={self.id}, "
            f"name={self.full_name}, "
            f"Email= {self.email}, "
            f"Phone={self.phone_number}, "
            f"Company={self.company_name}, "
            f"Created={self.creation_date}, "
            f"Last Contact:={self.last_contact}, "
            f"Commercial id={self.commercial_collaborator_id} \n"
        )
