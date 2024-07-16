from sqlalchemy import Column, Integer, String, Date, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base
from models.client import Client


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    commercial_contact = Column(String(100), nullable=True)
    total_amount = Column(Numeric, nullable=False)
    amount_due = Column(Numeric, nullable=False)
    creation_date = Column(Date, default=datetime.utcnow)
    status = Column(Boolean, nullable=False)

    client = relationship("Client", back_populates="contracts")

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
    def get_by_id(contract_id,session):
        return session.query(Contract).filter(Contract.id == contract_id).first()

    @staticmethod
    def get_all(session):
        return session.query(Contract).all()
    
    def __str__(self):
        return (f"Contract id={self.id}, client_id={self.client_id}, "
                f"commercial_contact='{self.commercial_contact}', total_amount={self.total_amount}, "
                f"amount_due={self.amount_due}, creation_date={self.creation_date}, "
                f"status={'signed' if self.status else 'unsigned'}")


Client.contracts = relationship(
    "Contract", order_by=Contract.id, back_populates="client"
)
