import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.user import User, UserRole
from app.utils import get_hashed_password

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    
    # Create a test admin user and an employee user
    db = TestingSessionLocal()
    admin = User(
        firstname="Admin",
        lastname="User",
        email="admin@test.com",
        hashed_password=get_hashed_password("adminpass"),
        role=UserRole.ADMIN,
        is_active=True
    )
    employee = User(
        firstname="Employee",
        lastname="User",
        email="employee@test.com",
        hashed_password=get_hashed_password("employeepass"),
        role=UserRole.EMPLOYEE,
        is_active=True
    )
    db.add(admin)
    db.add(employee)
    db.commit()
    
    yield db
    
    db.close()
    # Drop the database after tests are done
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
