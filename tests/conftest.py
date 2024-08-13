import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base
from models.client import Client
from models.collaborator import Collaborator, Role
from unittest.mock import patch
from click.testing import CliRunner
from epic_events import AuthGroup
from models.contract import Contract


# Configure the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Using SQLite for simplicity
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)  # Create tables for the test
    db = sessionmaker(bind=engine)()  # Create a new session
    try:
        yield db  # Provide the session to the test
        db.commit()  # Commit any changes made during the test
    except Exception:
        db.rollback()  # Rollback in case of error
        raise
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def collaborator(test_db):

    role = Role.get_or_create(test_db, name="sales")
    collaborator = Collaborator(
        id=1,
        name="Test Collaborator",
        email="collab@example.com",
        role_id=role.id,
        password="password",
    )
    collaborator.set_password("password")  # hash the password
    test_db.add(collaborator)
    test_db.commit()
    return collaborator


@pytest.fixture
def client(test_db, collaborator):

    client_data = {
        "id": 1,
        "full_name": "Foo floo",
        "email": "foofloo@example.com",
        "phone_number": "+33123456789",
        "company_name": "Example Corp",
        "commercial_collaborator_id": collaborator.id,
    }

    client = Client(**client_data)
    test_db.add(client)
    test_db.commit()  # Ensure transaction is committed
    return client


@pytest.fixture(scope="module")
def client_data():
    return {
        "full_name": "Foo Doe",
        "email": "foofloo@example.com",
        "phone_number": "+33123456789",
        "company_name": "Example Corp",
    }


@pytest.fixture
def mock_login_collaborator(collaborator):
    with patch("config.auth.get_login_collaborator", return_value=collaborator):
        yield


@pytest.fixture
def mock_auth_token():
    valid_token = "valid_token"
    valid_email = "collab@example.com"

    with patch("config.auth.get_token_from_file", return_value=valid_token):
        with patch(
            "config.auth.get_email_from_access_token", return_value=valid_email
        ):
            yield


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def client_unit():
    return Client(
        full_name="foo Doe",
        email="foo@example.com",
        phone_number="1234567890",
        company_name="ABC Corp",
    )


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
    with patch.object(
        AuthGroup,
        "invoke",
        lambda self, ctx: super(AuthGroup, self).invoke(ctx),
    ):
        yield


@pytest.fixture
def contract(test_db, client, collaborator):
    contract = Contract(
        client_id=client.id,
        commercial_collaborator_id=collaborator.id,
        total_amount=10000.00,
        amount_due=5000.00,
        status=True,
    )
    contract.save(test_db)
    return contract
