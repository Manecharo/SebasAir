import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create a test database session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a mock database session
@pytest.fixture
def mock_db():
    """Create a mock database session for testing."""
    return MagicMock(spec=Session) 