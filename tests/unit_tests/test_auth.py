from unittest.mock import patch, mock_open
from datetime import datetime, timedelta, timezone
from config.auth import (
    is_token_expired,
    get_email_from_access_token,
    get_token_from_file,
    create_access_token,
    get_login_collaborator,
    is_authenticated,
    has_permission,
)


def test_is_token_expired(mock_jwt_decode, mock_datetime_now):
    # Mock the decoded payload
    mock_payload = {"exp": 1672531200}  # Expiration time: 2023-01-01 00:00:00 UTC
    mock_jwt_decode.return_value = mock_payload

    # Mock the current time
    mock_now = datetime(2022, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    mock_datetime_now.return_value = mock_now

    # Token should not be expired
    assert not is_token_expired("dummy_token", "dummy_secret_key")

    # Mock the current time to be after the expiration time
    mock_now = datetime(2023, 1, 1, 0, 0, 1, tzinfo=timezone.utc)
    mock_datetime_now.return_value = mock_now

    # Token should be expired
    assert is_token_expired("dummy_token", "dummy_secret_key")


def test_get_email_from_access_token(mock_jwt_decode):
    # Mock the decoded payload
    mock_payload = {"sub": "test@example.com"}
    mock_jwt_decode.return_value = mock_payload

    # Get email from access token
    email = get_email_from_access_token("dummy_token")

    # Assert email is correct
    assert email == "test@example.com"


def test_get_token_from_file():
    # Mock the file read operation
    m = mock_open(read_data="dummy_token")
    with patch("builtins.open", m):
        # Get token from file
        token = get_token_from_file()

        # Assert token is correct
        assert token == "dummy_token"


def test_create_access_token(mock_jwt_encode, mock_datetime_now, mock_os_makedirs):
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    SECRET_KEY = "dummy_secret_key"
    ALGORITHM = "HS256"
    # Mock the encoded token
    mock_encoded_token = "dummy_encoded_token"
    mock_jwt_encode.return_value = mock_encoded_token

    # Mock the current time
    mock_now = datetime(2022, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    mock_datetime_now.return_value = mock_now

    # Mock the os.makedirs function
    mock_os_makedirs.return_value = None

    # Mock the file write operation
    m = mock_open()
    with patch("builtins.open", m), patch(
        "config.auth.ACCESS_TOKEN_EXPIRE_MINUTES", ACCESS_TOKEN_EXPIRE_MINUTES
    ), patch("config.auth.SECRET_KEY", SECRET_KEY), patch(
        "config.auth.ALGORITHM", ALGORITHM
    ):
        # Call the function
        access_token = create_access_token({"data": "dummy_data"})

        # Assert access token is correct
        assert access_token == mock_encoded_token

        # Assert the function calls
        mock_jwt_encode.assert_called_once_with(
            {
                "data": "dummy_data",
                "exp": mock_now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            },
            SECRET_KEY,
            algorithm=ALGORITHM,
        )
        mock_os_makedirs.assert_called_once_with(
            '~/tmp',
            exist_ok=True,
        )
        m.assert_called_once_with(
            '~/tmp/access_token',
            "w",
        )
        m().write.assert_called_once_with(mock_encoded_token)


def test_get_login_collaborator(
    mock_get_token_from_file,
    mock_get_email_from_access_token,
    mock_Collaborator,
):
    # Mock the token and email
    mock_token = "dummy_token"
    mock_get_token_from_file.return_value = mock_token
    mock_email = "test@example.com"
    mock_get_email_from_access_token.return_value = mock_email

    # Mock the Collaborator instance
    mock_collaborator = mock_Collaborator.get_by_email.return_value

    # Call the function
    collaborator = get_login_collaborator("dummy_session")

    # Assert the Collaborator instance is returned
    assert collaborator == mock_collaborator

    # Assert the function calls
    mock_get_token_from_file.assert_called_once()
    mock_get_email_from_access_token.assert_called_once_with(mock_token)
    mock_Collaborator.get_by_email.assert_called_once_with(
        email=mock_email, session="dummy_session"
    )


def test_is_authenticated(mock_get_token_from_file, mock_is_token_expired):
    SECRET_KEY = "dummy_secret_key"
    # Mock the token file not found scenario
    mock_get_token_from_file.side_effect = FileNotFoundError

    # Call the function
    authenticated = is_authenticated()

    # Assert token file not found scenario
    assert not authenticated
    mock_get_token_from_file.assert_called_once()

    mock_get_token_from_file.reset_mock()
    mock_is_token_expired.reset_mock()
    # Mock the token expired scenario
    mock_get_token_from_file.side_effect = None
    mock_is_token_expired.return_value = True

    # Call the function
    with patch("config.auth.SECRET_KEY", SECRET_KEY):
        authenticated = is_authenticated()

    # Assert token expired scenario
    assert not authenticated
    assert mock_get_token_from_file.call_count == 1
    mock_is_token_expired.assert_called_with(
        mock_get_token_from_file.return_value, SECRET_KEY
    )

    mock_get_token_from_file.reset_mock()
    # Mock the valid token scenario
    mock_get_token_from_file.side_effect = None
    mock_is_token_expired.return_value = False

    # Call the function
    with patch("config.auth.SECRET_KEY", SECRET_KEY):
        authenticated = is_authenticated()

    # Assert valid token scenario
    assert authenticated
    assert mock_get_token_from_file.call_count == 1
    mock_is_token_expired.assert_called_with(
        mock_get_token_from_file.return_value, SECRET_KEY
    )


def test_has_permission(mock_get_login_collaborator):
    # Mock the login collaborator
    mock_collaborator = mock_get_login_collaborator.return_value
    mock_collaborator.role.permissions = ["permission1", "permission2"]

    # Check if has permission
    has_perm = has_permission("permission1", "dummy_session")

    # Assert has permission is True
    assert has_perm

    # Check if does not have permission
    has_perm = has_permission("permission3", "dummy_session")

    # Assert has permission is False
    assert not has_perm
    # Assert the function calls
    mock_get_login_collaborator.assert_called_with(session="dummy_session")
    assert mock_collaborator.role.permissions == ["permission1", "permission2"]
