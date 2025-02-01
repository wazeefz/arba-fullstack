# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Secure Database URL (use environment variable or .env file)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/mydb")

# Create SQLAlchemy engine (No `connect_args` for PostgreSQL)
engine = create_engine(DATABASE_URL)

# Create a session local to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create tables (Optional, can be run at startup)
def init_db():
    from models import Base  # Import models to ensure they are registered
    Base.metadata.create_all(bind=engine)
