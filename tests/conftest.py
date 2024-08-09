import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine, __version__ as sqlalchemy_version
from sqlalchemy.orm import sessionmaker
from config.database import Base
from models.client import Client
from models.collaborator import Collaborator, Role
from unittest.mock import patch
from click.testing import CliRunner
from epic_events import cli, AuthGroup

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

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def client():
    return Client(full_name="foo Doe", email="foo@example.com", phone_number="1234567890", company_name="ABC Corp")


@pytest.fixture
def mock_jwt_decode():
    with patch("config.auth.jwt.decode") as mock_decode:
        yield mock_decode

@pytest.fixture
def mock_jwt_encode():
    with patch("config.auth.jwt.encode") as mock_decode:
        yield mock_decode

@pytest.fixture
def mock_datetime_now():
    with patch("config.auth.datetime") as mock_datetime:
        yield mock_datetime.now

# @pytest.fixture
# def mock_os_makedirs():
#     with patch("os.makedirs") as mock_makedirs:
#         yield mock_makedirs


@pytest.fixture
def mock_jwt_decode():
    with patch("config.auth.jwt.decode") as mock_decode:
        yield mock_decode


@pytest.fixture
def mock_os_makedirs():
    with patch("config.auth.os.makedirs") as mock_makedirs:
        yield mock_makedirs


@pytest.fixture
def mock_get_token_from_file():
    with patch("config.auth.get_token_from_file") as mock_get_token:
        yield mock_get_token


@pytest.fixture
def mock_get_email_from_access_token():
    with patch("config.auth.get_email_from_access_token") as mock_get_email:
        yield mock_get_email


@pytest.fixture
def mock_Collaborator():
    with patch("config.auth.Collaborator") as mock_collaborator:
        yield mock_collaborator

@pytest.fixture
def mock_is_token_expired():
    with patch("config.auth.is_token_expired") as mock_is_expired:
        yield mock_is_expired

@pytest.fixture
def mock_get_login_collaborator():
    with patch("config.auth.get_login_collaborator") as mock_get_login:
        yield mock_get_login

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_invoke():
    with patch.object(AuthGroup, 'invoke', lambda self, ctx: super(AuthGroup, self).invoke(ctx)):
        yield
