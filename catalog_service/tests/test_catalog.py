"""
Tests for Catalog Service.
Covers SCRUM-101 (add vehicle), SCRUM-106 (listing), SCRUM-107 (detail),
SCRUM-109 (vehicle model), and SCRUM-163 (test setup).
The Auth Service REST call is mocked in unit tests to keep them fast and isolated.
A real cross-service integration test lives in /tests/test_integration.py.
"""
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db


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
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def valid_token_payload():
    return {
        "valid": True,
        "user_id": 1,
        "email": "test@example.com",
        "role": "customer",
    }


def _sample_vehicle_payload():
    return {
        "brand": "Tesla",
        "model": "Model 3",
        "year": 2023,
        "mileage": 15000,
        "price": "42500.00",
        "fuel_type": "electric",
    }


# ---------- Listing endpoint (SCRUM-106) ----------

def test_list_vehicles_empty(client):
    response = client.get("/api/vehicles")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_list_vehicles_with_items(client, valid_token_payload):
    # Add two vehicles via the protected endpoint
    with patch(
        "app.core.auth_client.verify_token_with_auth_service",
        new=AsyncMock(return_value=valid_token_payload),
    ):
        for i in range(2):
            payload = _sample_vehicle_payload()
            payload["model"] = f"Model {i}"
            client.post(
                "/api/vehicles",
                json=payload,
                headers={"Authorization": "Bearer fake-token"},
            )

    response = client.get("/api/vehicles")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


# ---------- Detail endpoint (SCRUM-107) ----------

def test_get_vehicle_not_found(client):
    response = client.get("/api/vehicles/999")
    assert response.status_code == 404


def test_get_vehicle_by_id(client, valid_token_payload):
    with patch(
        "app.core.auth_client.verify_token_with_auth_service",
        new=AsyncMock(return_value=valid_token_payload),
    ):
        create_resp = client.post(
            "/api/vehicles",
            json=_sample_vehicle_payload(),
            headers={"Authorization": "Bearer fake-token"},
        )
        vehicle_id = create_resp.json()["id"]

    response = client.get(f"/api/vehicles/{vehicle_id}")
    assert response.status_code == 200
    assert response.json()["brand"] == "Tesla"


# ---------- Create endpoint (SCRUM-101) ----------

def test_create_vehicle_requires_auth(client):
    response = client.post("/api/vehicles", json=_sample_vehicle_payload())
    assert response.status_code in (401, 403)  # HTTPBearer missing


def test_create_vehicle_with_valid_token(client, valid_token_payload):
    with patch(
        "app.core.auth_client.verify_token_with_auth_service",
        new=AsyncMock(return_value=valid_token_payload),
    ) as mock_verify:
        response = client.post(
            "/api/vehicles",
            json=_sample_vehicle_payload(),
            headers={"Authorization": "Bearer fake-token"},
        )

    assert response.status_code == 201
    # Confirm Catalog actually called Auth Service via REST
    mock_verify.assert_awaited_once_with("fake-token")
    data = response.json()
    assert data["brand"] == "Tesla"
    assert data["status"] == "available"


def test_create_vehicle_with_invalid_token(client):
    from fastapi import HTTPException, status

    async def mock_verify_fail(token: str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    with patch(
        "app.core.auth_client.verify_token_with_auth_service",
        side_effect=mock_verify_fail,
    ):
        response = client.post(
            "/api/vehicles",
            json=_sample_vehicle_payload(),
            headers={"Authorization": "Bearer bad-token"},
        )

    assert response.status_code == 401


def test_create_vehicle_validation_year(client, valid_token_payload):
    payload = _sample_vehicle_payload()
    payload["year"] = 1980  # Below allowed range

    with patch(
        "app.core.auth_client.verify_token_with_auth_service",
        new=AsyncMock(return_value=valid_token_payload),
    ):
        response = client.post(
            "/api/vehicles",
            json=payload,
            headers={"Authorization": "Bearer fake-token"},
        )
    assert response.status_code == 422


def test_create_vehicle_validation_negative_mileage(client, valid_token_payload):
    payload = _sample_vehicle_payload()
    payload["mileage"] = -100

    with patch(
        "app.core.auth_client.verify_token_with_auth_service",
        new=AsyncMock(return_value=valid_token_payload),
    ):
        response = client.post(
            "/api/vehicles",
            json=payload,
            headers={"Authorization": "Bearer fake-token"},
        )
    assert response.status_code == 422


# ---------- HTML pages (SCRUM-106, 107) ----------

def test_listing_page_renders(client):
    response = client.get("/vehicles")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Browse the Inventory" in response.text


def test_detail_page_404(client):
    response = client.get("/vehicles/9999")
    assert response.status_code == 404
    assert "not found" in response.text.lower()


def test_add_vehicle_form_renders(client):
    response = client.get("/admin/add-vehicle")
    assert response.status_code == 200
    assert "Add a Vehicle" in response.text


# ---------- Health check ----------

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "catalog_service"
