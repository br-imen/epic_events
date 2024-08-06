import os
import sys
from config.database import Base,engine

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

Base.metadata.create_all(bind=engine)
print("tables created")