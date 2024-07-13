from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from config.database import Base, SessionLocal


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    description = Column(String, nullable=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    support_contact_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)

    def save(self):
        SessionLocal.add(self)
        SessionLocal.commit()

    def update(self):
        SessionLocal.merge(self)
        SessionLocal.commit()

    def delete(self):
        SessionLocal.delete(self)
        SessionLocal.commit()

    @staticmethod
    def get_all():
        return SessionLocal.query(Event).all()
