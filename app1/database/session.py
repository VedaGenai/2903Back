from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from app1.core.config import DATABASE_URL, DATABASE_POOL_SIZE, DATABASE_MAX_OVERFLOW
from typing import Generator

# Create declarative base for models
Base = declarative_base()

# Create engine
engine = create_engine(
    DATABASE_URL, 
    pool_size=DATABASE_POOL_SIZE,
    max_overflow=DATABASE_MAX_OVERFLOW
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db() -> Generator[Session, None, None]:
    """
    Dependency that creates a new database session for each request
    and closes it after the request is completed
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database by creating all tables defined in the models
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")