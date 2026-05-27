"""
Tests for Auth Service.
Implements SCRUM-86 subtask SCRUM-92 + SCRUM-88 subtask SCRUM-105.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db


# In-memory SQLite for fast, isolated tests
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    """Create fresh tables for each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


# ---------- Register tests ----------

def test_register_success(client):
    response = client.post(
        "/register",
        json={"email": "alice@example.com", "password": "securepass123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["role"] == "customer"
    assert "id" in data
    assert "hashed_password" not in data  # never leak password hash


def test_register_short_password(client):
    response = client.post(
        "/register",
        json={"email": "bob@example.com", "password": "short"},
    )
    assert response.status_code == 422  # Pydantic validation error


def test_register_invalid_email(client):
    response = client.post(
        "/register",
        json={"email": "not-an-email", "password": "validpass123"},
    )
    assert response.status_code == 422


def test_register_duplicate_email(client):
    client.post("/register", json={"email": "dup@example.com", "password": "validpass123"})
    response = client.post(
        "/register",
        json={"email": "dup@example.com", "password": "anothervalidpass"},
    )
    assert response.status_code == 409


# ---------- Login tests ----------

def test_login_success(client):
    client.post(
        "/register",
        json={"email": "charlie@example.com", "password": "mypassword123"},
    )
    response = client.post(
        "/login",
        json={"email": "charlie@example.com", "password": "mypassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "charlie@example.com"


def test_login_wrong_password(client):
    client.post(
        "/register",
        json={"email": "dave@example.com", "password": "correctpassword"},
    )
    response = client.post(
        "/login",
        json={"email": "dave@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/login",
        json={"email": "ghost@example.com", "password": "anypassword"},
    )
    assert response.status_code == 401


# ---------- Verify endpoint tests ----------

def test_verify_valid_token(client):
    client.post(
        "/register",
        json={"email": "eve@example.com", "password": "evespassword"},
    )
    login_resp = client.post(
        "/login",
        json={"email": "eve@example.com", "password": "evespassword"},
    )
    token = login_resp.json()["access_token"]

    response = client.get(
        "/verify",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["email"] == "eve@example.com"
    assert data["role"] == "customer"


def test_verify_invalid_token(client):
    response = client.get(
        "/verify",
        headers={"Authorization": "Bearer this-is-not-a-real-token"},
    )
    assert response.status_code == 401


def test_verify_missing_token(client):
    response = client.get("/verify")
    # HTTPBearer with no credentials returns 401 (Not authenticated) in newer FastAPI
    assert response.status_code in (401, 403)


# ---------- Password hashing isolation tests ----------

def test_password_is_hashed(client):
    """Password should never be stored or returned in plain text."""
    response = client.post(
        "/register",
        json={"email": "frank@example.com", "password": "secretpassword"},
    )
    body = response.json()
    # Plain password must not appear anywhere in response
    assert "secretpassword" not in str(body)
    assert "hashed_password" not in body


# ---------- Health check ----------

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
