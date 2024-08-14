from sqlalchemy import (
    Column,
    Integer,
    Date,
    Boolean,
    Numeric,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base


class Contract(Base):
    """
    Represents a contract in the system.

    Attributes:
        id (int): The unique identifier of the contract.
        client_id (int): The ID of the client associated with the contract.
        commercial_collaborator_id (int): The ID of the commercial collaborator
        associated with the contract.
        total_amount (decimal.Decimal): The total amount of the contract.
        amount_due (decimal.Decimal): The amount due for the contract.
        creation_date (datetime.date): The creation date of the contract.
        status (bool): The status (True if signed, False if unsigned).
        client (Client): The client associated with the contract.
        collaborator (Collaborator): The commercial collaborator associated with
        the contract.
        event (Event): The event associated with the contract.
    """

    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    commercial_collaborator_id = Column(Integer, ForeignKey("collaborators.id"))
    total_amount = Column(Numeric, nullable=False)
    amount_due = Column(Numeric, nullable=False)
    creation_date = Column(Date, default=datetime.utcnow)
    status = Column(Boolean, nullable=False)
    client = relationship("Client", back_populates="contracts")
    collaborator = relationship(
        "Collaborator", back_populates="contracts"
    )  # Sales collaborator
    event = relationship(
        "Event", order_by="Event.id", back_populates="contract", uselist=False
    )

    def save(self, session):
        """
        Saves the contract to the database.

        Args:
            session (Session): The database session.

        Returns:
            None
        """
        session.add(self)
        session.commit()

    def update(self, session, **kwargs):
        """
        Updates the contract with the specified attributes.

        Args:
            session (Session): The database session.
            **kwargs: The attributes to update.

        Returns:
            None
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.merge(self)
        session.commit()

    def delete(self, session):
        """
        Deletes the contract from the database.

        Args:
            session (Session): The database session.

        Returns:
            None
        """
        session.delete(self)
        session.commit()

    @staticmethod
    def get_by_id(contract_id, session):
        """
        Retrieves a contract by its ID.

        Args:
            contract_id (int): The ID of the contract.
            session (Session): The database session.

        Returns:
            Contract: The contract with the specified ID, or None if not found.
        """
        return session.query(Contract).filter(Contract.id == contract_id).first()

    @staticmethod
    def get_all(session, filters):
        """
        Retrieves all contracts based on the specified filters.

        Args:
            session (Session): The database session.
            filters (list): The filters to apply.

        Returns:
            list: A list of contracts that match the filters.
        """
        contracts = session.query(Contract)
        if "unpaid" in filters:
            contracts = contracts.filter(Contract.amount_due != 0)
        if "unsigned" in filters:
            contracts = contracts.filter(Contract.status.is_(False))
        return contracts.all()

    def __str__(self):
        """
        Returns a string representation of the contract.

        Returns:
            str: The string representation of the contract.
        """
        return (
            f"Contract id={self.id}, client_id={self.client_id}, "
            f"commercial_id='{self.commercial_collaborator_id}', "
            f"commercial='{self.collaborator.name}', "
            f"total_amount={self.total_amount}, "
            f"amount_due={self.amount_due}, "
            f"creation_date={self.creation_date}, "
            f"status={'signed' if self.status else 'unsigned'}"
        )
