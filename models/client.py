from sqlalchemy import Column, Integer, String, DateTime
from config.database import SessionLocal, Base
from datetime import datetime


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    company_name = Column(String)
    creation_date = Column(DateTime, default=datetime.utcnow)
    last_contact = Column(DateTime)
    contact_commercial = Column(String)

    # Active Record CRUD Methods
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
    def get_by_id(client_id):
        return SessionLocal.query(Client).filter(Client.id == client_id).first()

    @staticmethod
    def get_all():
        return SessionLocal.query(Client).all()
