from config.database import engine, Base
from models import Client,Collaborator,Event,Contract

# Create all tables in the target database
Base.metadata.create_all(bind=engine)
print("Tables created successfully")
