import psycopg2
from psycopg2 import sql
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection details
admin_user = os.getenv("DB_USER")
admin_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
default_db = os.getenv("DEFAULT_DB")


# Connect to the PostgreSQL server
def create_db():
    try:
        # Connect to the default database (usually 'postgres')
        conn = psycopg2.connect(
            dbname=default_db,
            user="postgres",
            password="postgres",
            host="localhost",
        )
        conn.autocommit = True  # Enable autocommit so we can create a new database
        cursor = conn.cursor()

        # Create user if it doesn't exist
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_roles WHERE rolname=%s"), [admin_user]
        )
        if not cursor.fetchone():
            print(f"Creating user '{admin_user}'...")
            cursor.execute(
                sql.SQL("CREATE USER {user} WITH PASSWORD %s").format(
                    user=sql.Identifier(admin_user)
                ),
                [admin_password],
            )
        else:
            print(f"User '{admin_user}' already exists.")

        # Create database if it doesn't exist
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname=%s"), [db_name]
        )
        if not cursor.fetchone():
            print(f"Creating database '{db_name}'...")
            cursor.execute(
                sql.SQL("CREATE DATABASE {dbname} OWNER {user}").format(
                    dbname=sql.Identifier(db_name), user=sql.Identifier(admin_user)
                )
            )
        else:
            print(f"Database '{db_name}' already exists.")

        cursor.close()
        conn.close()
        print("Database and user setup completed successfully.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if (
        input("This will create a new database and user." "Are you sure? (yes/no): ")
        .strip()
        .lower()
        == "yes"
    ):
        create_db()
    else:
        print("Operation aborted.")
