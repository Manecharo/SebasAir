import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Use SQLite in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create a mock for the database dependency
@pytest.fixture
def mock_db():
    db = MagicMock()
    yield db

# Patch the get_db dependency
@pytest.fixture(autouse=True)
def override_get_db():
    with patch("src.config.db.get_db") as _get_db:
        mock_session = MagicMock()
        _get_db.return_value = mock_session
        yield _get_db

# Patch the Base.metadata.create_all function to prevent database creation
@pytest.fixture(autouse=True, scope="session")
def override_create_all():
    with patch("sqlalchemy.ext.declarative.declarative_base") as mock_base:
        mock_metadata = MagicMock()
        mock_base.return_value.metadata = mock_metadata
        yield mock_base

# Override the get_db dependency
@pytest.fixture
def client(mock_db):
    """Create a test client with a mocked database session."""
    def override_get_db():
        yield mock_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    # Reset the dependency override after the test
    app.dependency_overrides = {} 