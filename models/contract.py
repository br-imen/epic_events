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
    events = relationship("Event", order_by="Event.id", back_populates="contract")

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
    def get_by_id(contract_id, session):
        return session.query(Contract).filter(Contract.id == contract_id).first()

    @staticmethod
    def get_all(session, filters):
        contracts = session.query(Contract)
        if "unpaid" in filters:
            contracts = contracts.filter(Contract.amount_due != 0)
        if "unsigned" in filters:
            contracts = contracts.filter(Contract.status.is_(False))
        return contracts.all()

    def __str__(self):
        return (
            f"Contract id={self.id}, client_id={self.client_id}, "
            f"commercial_id='{self.commercial_collaborator_id}', "
            f"commercial='{self.collaborator.name}', "
            f"total_amount={self.total_amount}, "
            f"amount_due={self.amount_due}, "
            f"creation_date={self.creation_date}, "
            f"status={'signed' if self.status else 'unsigned'}"
        )
