import enum
import bcrypt
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    Enum as SqlEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from config.database import Base


class RoleEnum(enum.Enum):
    """
    Enum representing the different roles available in the system.

    Attributes:
        sales (str): Represents the sales role.
        support (str): Represents the support role.
        management (str): Represents the management role.
    """

    sales = "sales"
    support = "support"
    management = "management"


# Association table for the many-to-many relationship between roles and permissions.
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id")),
)


class Role(Base):
    """
    Represents a role within the system.

    Attributes:
        id (int): The primary key for the role.
        name (RoleEnum): The name of the role, using the RoleEnum enum.
        collaborators (list of Collaborator): A list of collaborators associated
        with the role.
        permissions (list of Permission): A list of permissions associated
        with the role.
    """

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(SqlEnum(RoleEnum), nullable=False, unique=True)
    collaborators = relationship("Collaborator", back_populates="role")

    permissions = relationship(
        "Permission", secondary=role_permissions, back_populates="roles"
    )

    def save(self, session):
        session.add(self)
        session.commit()

    @staticmethod
    def get_by_id(id, session):
        return session.query(Role).filter(Role.id == id).first()

    @classmethod
    def get_or_create(cls, session, name):
        instance = session.query(cls).filter_by(name=name).first()
        if instance:
            return instance
        instance = cls(name=name)
        session.add(instance)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            instance = session.query(cls).filter_by(name=name).first()
        return instance

    def __str__(self) -> str:
        return self.name.value


class Permission(Base):
    """
    Represents a permission within the system.

    Attributes:
        id (int): The primary key for the permission.
        name (str): The name of the permission, which must be unique and not null.
        roles (list of Role): A list of roles associated with this permission,
        using a many-to-many relationship.
    """

    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    roles = relationship(
        "Role", secondary=role_permissions, back_populates="permissions"
    )

    def save(self, session):
        session.add(self)
        session.commit()

    @classmethod
    def get_or_create(cls, session, name):
        """
        Retrieves a permission by name, or creates it if it doesn't exist.

        Args:
            session (Session): The SQLAlchemy session object used to interact
            with the database.
            name (str): The name of the permission to retrieve or create.

        Returns:
            Permission: The existing or newly created permission instance.
        """
        instance = session.query(cls).filter_by(name=name).first()
        if instance:
            return instance
        instance = cls(name=name)
        session.add(instance)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            instance = session.query(cls).filter_by(name=name).first()
        return instance

    def __str__(self) -> str:
        return self.name


class Collaborator(Base):
    """
    Represents a collaborator (employee) in the system.

    Attributes:
        id (int): The primary key for the collaborator.
        employee_number (int): The unique employee number of the collaborator.
        name (str): The full name of the collaborator.
        email (str): The email address of the collaborator.
        role_id (int): Foreign key referencing the role of the collaborator.
        password (str): The hashed password of the collaborator.
        contracts (list of Contract): A list of contracts associated with
        the collaborator.
        events (list of Event): A list of events where the collaborator
        provided support.
        clients (list of Client): A list of clients managed by the collaborator.
        role (Role): The role assigned to the collaborator.
    """

    __tablename__ = "collaborators"
    id = Column(Integer, primary_key=True)
    employee_number = Column(Integer, index=True, unique=True)
    name = Column(String(100), nullable=False)
    email = Column(String, nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    password = Column(String, nullable=False)
    contracts = relationship("Contract", back_populates="collaborator")
    events = relationship(
        "Event", order_by="Event.id", back_populates="collaborator_support"
    )
    clients = relationship("Client", back_populates="collaborator")
    role = relationship("Role", back_populates="collaborators")

    def set_password(self, password):
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password.encode("utf-8")
        )

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
            f"Collaborator id={self.id}, "
            f"employee_number={self.employee_number}, "
            f"name={self.name}, "
            f"email={self.email}, "
            f"role={str(self.role)})  \n"
        )

    @staticmethod
    def get_by_id(id, session):
        return session.query(Collaborator).filter(Collaborator.id == id).first()

    @staticmethod
    def get_by_employee_number(employee_number, session):
        return (
            session.query(Collaborator)
            .filter(Collaborator.employee_number == employee_number)
            .first()
        )

    @staticmethod
    def get_by_email(email, session):
        return (
            session.query(Collaborator).filter(Collaborator.email == email).first()
        )

    @staticmethod
    def get_all(session):
        return session.query(Collaborator).all()
