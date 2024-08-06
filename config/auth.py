from functools import wraps
import os
import jwt
from datetime import datetime, timedelta, timezone

from models.collaborator import Collaborator


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Create token and save it in ~/.config/epic_events/access_token.txt
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "epic_events")
    os.makedirs(config_dir, exist_ok=True)
    token_path = os.path.join(config_dir, "access_token.txt")
    with open(token_path, "w") as file:
        file.write(encoded_jwt)
    return encoded_jwt


# Return email from token
def get_email_from_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise ValueError("Email not found in token")
        return email
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


# Get token from folder
def get_token_from_file():
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "epic_events")
    token_path = os.path.join(config_dir, "access_token.txt")

    if os.path.exists(token_path):
        with open(token_path, "r") as file:
            token = file.read().strip()
        return token
    else:
        raise FileNotFoundError("Token file not found")


# Check if token expired
def is_token_expired(token, secret_key):
    try:
        # Decode the token without verifying the signature to access the payload
        payload = jwt.decode(
            token, secret_key, algorithms=["HS256"], options={"verify_signature": False}
        )

        # Get the expiration time from the payload
        exp = payload.get("exp")

        if exp is None:
            raise ValueError("Token does not contain an expiration claim.")

        # Get the current time
        now = datetime.now(timezone.utc).timestamp()

        # Check if the token is expired
        if now > exp:
            return True
        else:
            return False

    except jwt.ExpiredSignatureError:
        # If the token has expired according to PyJWT's built-in check
        return True
    except jwt.InvalidTokenError as e:
        # If the token is otherwise invalid
        raise ValueError(f"Invalid token: {e}")

def get_login_collaborator(session):
    token = get_token_from_file()
    email = get_email_from_access_token(token)
    collaborator = Collaborator.get_by_email(email=email, session=session)
    return collaborator

def is_authenticated():
    try:
        token = get_token_from_file()
    except FileNotFoundError:
        print("Token file not found.")
        return False

    if is_token_expired(token, SECRET_KEY):
        print("Token has expired.")
        return False
    return True


def has_permission(command, session):
    collaborator = get_login_collaborator(session=session)
    role = collaborator.role
    permissions = role.permissions
    permissions_names = [str(permission) for permission in permissions]
    if command in permissions_names:
        return True
    return False
