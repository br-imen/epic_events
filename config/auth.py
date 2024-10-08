import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone

from models.collaborator import Collaborator
load_dotenv()
# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# Create token and save it in ~/.config/epic_events/access_token.txt
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    home_directory = os.path.expanduser("~")
    token_dir_path = os.path.join(home_directory, os.getenv("TOKEN_DIR_PATH"))
    os.makedirs(token_dir_path, exist_ok=True)

    token_path = os.path.join(token_dir_path, os.getenv("TOKEN_FILENAME"))
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
    home_directory = os.path.expanduser("~")
    token_path = os.path.join(home_directory, os.getenv("TOKEN_DIR_PATH"),
                              os.getenv("TOKEN_FILENAME"))
    if os.path.exists(token_path):
        with open(token_path, "r") as file:
            token = file.read().strip()
        return token
    else:
        raise FileNotFoundError("Token file not found")


# Check if token expired
def is_token_expired(token, secret_key):
    try:
        # Decode the token without verifying the signature
        # to access the payload
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=["HS256"],
            options={"verify_signature": False},
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


# Retrieves the currently logged-in collaborator from the database using the email
# extracted from the JWT token.
def get_login_collaborator(session):
    token = get_token_from_file()
    email = get_email_from_access_token(token)
    collaborator = Collaborator.get_by_email(email=email, session=session)
    return collaborator


# Checks if the current JWT token is present and valid
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


# Verifies if the currently logged-in collaborator has permission to execute the
# specified command based on their assigned role and permissions in the system.
def has_permission(command, session):
    collaborator = get_login_collaborator(session=session)
    role = collaborator.role
    permissions = role.permissions
    permissions_names = [str(permission) for permission in permissions]
    if command in permissions_names:
        return True
    return False
