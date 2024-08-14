import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.database import Base, engine  # noqa: E402
from config.database import SessionLocal  # noqa: E402
from config.permissions import ROLES_PERMISSIONS  # noqa: E402
from models.collaborator import Collaborator, Permission, Role  # noqa: E402


# Create the database tables
Base.metadata.create_all(bind=engine)

# Create the default roles and permissions
session = SessionLocal()
for role, permissions in ROLES_PERMISSIONS.items():
    role_instance = Role.get_or_create(session, role)
    for permission in permissions:
        permission_instance = Permission.get_or_create(session, permission)
        permission_instance.save(session)
        role_instance.permissions.append(permission_instance)
        role_instance.save(session)

# Create the superuser
collaborator_email = os.getenv("SUPER_USER_EMAIL")
existing_collaborator = (
    session.query(Collaborator).filter_by(email=collaborator_email).first()
)

if not existing_collaborator:
    collaborator = Collaborator(
        email=collaborator_email,
        name=os.getenv("SUPER_USER"),
        password=os.getenv("SUPER_USER_PASSWORD"),
        role_id=3,
    )
    collaborator.save(session)
