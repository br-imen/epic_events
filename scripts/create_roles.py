import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.database import SessionLocal, ROLES_PERMISSIONS
from models.collaborator import Permission, Role

def main():
    session = SessionLocal()
    for role, permissions in ROLES_PERMISSIONS.items():
        role_instance = Role.get_or_create(session, role)
        for permission in permissions:
            permission_instance = Permission.get_or_create(session, permission)
            permission_instance.save(session)
            role_instance.permissions.append(permission_instance)
            role_instance.save(session)



if __name__ == "__main__":
    main()

