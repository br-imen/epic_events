import enum
import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum as SqlEnum
from sqlalchemy.orm import relationship
from config.database import SessionLocal, Base


class RoleEnum(enum.Enum):
    sales = "sales"
    support = "support"
    management = "management"


# Association table for Role and Permission
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id")),
)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(SqlEnum(RoleEnum), nullable=False)

    permissions = relationship(
        "Permission", secondary=role_permissions, back_populates="roles"
    )

    def save(self, session):
        session.add(self)
        session.commit()


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    roles = relationship(
        "Role", secondary=role_permissions, back_populates="permissions"
    )


class Collaborator(Base):
    __tablename__ = "collaborators"

    id = Column(Integer, primary_key=True)
    employee_number = Column(Integer, index=True, unique=True)
    name = Column(String(100), nullable=False)
    email = Column(String, nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    password = Column(String, nullable=False)

    def set_password(self, password):
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def save(self, session):
        self.set_password(self.password)  # Ensure password is hashed before saving
        session.add(self)
        session.commit()

    def update(self, session, **kwargs):
        if "password" in kwargs:
            self.set_password(kwargs["password"])  # Hash the new password
            kwargs.pop("password")

        for key, value in kwargs.items():
            setattr(self, key, value)

        session.merge(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __str__(self):
        return (
            f"Collaborator {self.id}, employee_number={self.employee_number}, "
            f"name={self.name}, email={self.email}, role={self.role_id})"
        )

    @staticmethod
    def get_by_id(employee_number, session):
        return (
            session.query(Collaborator)
            .filter(Collaborator.employee_number == employee_number)
            .first()
        )

    @staticmethod
    def get_by_email(email, session):
        return session.query(Collaborator).filter(Collaborator.email == email).first()

    @staticmethod
    def get_by_name(name, session):
        return session.query(Collaborator).filter(Collaborator.name == name).first()

    @staticmethod
    def get_all(session):
        return session.query(Collaborator).all()
