import pytest
from sqlalchemy import create_engine, __version__ as sqlalchemy_version
from sqlalchemy.orm import sessionmaker
from config.database import Base
from models.client import Client
from models.collaborator import Collaborator, Role
from unittest.mock import patch

print("SQLAlchemy version:", sqlalchemy_version)

# Setup in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="session")
def engine_fixture():
    return engine

@pytest.fixture(scope="session")
def connection(engine_fixture):
    connection = engine_fixture.connect()
    yield connection
    connection.close()

@pytest.fixture
def session(connection):
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()

@pytest.fixture
def collaborator(session):
    role = Role.get_or_create(session, name="sales")
    collaborator = Collaborator(id=1, name="Test Collaborator", email="collab@example.com", role_id=role.id, password="password")
    collaborator.set_password("password")  # hash the password
    session.add(collaborator)
    session.commit()
    return collaborator

@pytest.fixture
def mock_login_collaborator(collaborator):
    with patch("config.auth.get_login_collaborator", return_value=collaborator):
        yield

@pytest.fixture
def mock_session_local(session):
    with patch("controllers.client_controller.SessionLocal", return_value=session):
        yield


@pytest.fixture
def mock_auth_token():
    valid_token = "valid_token"
    valid_email = "collab@example.com"

    with patch("config.auth.get_token_from_file", return_value=valid_token):
        with patch("config.auth.get_email_from_access_token", return_value=valid_email):
            yield
