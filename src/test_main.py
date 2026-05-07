from fastapi.testclient import TestClient

from main import Base, engine, app

client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def register_and_login(username="student", password="password123"):
    register_response = client.post(
        "/register",
        data={"username": username, "password": password},
        follow_redirects=False,
    )
    assert register_response.status_code == 303

    login_response = client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )
    assert login_response.status_code == 303


def test_home_page_loads():
    response = client.get("/")

    assert response.status_code == 200
    assert "Car Store Management System" in response.text


def test_user_can_register_login_and_view_empty_inventory():
    register_and_login()

    response = client.get("/vehicles")

    assert response.status_code == 200
    assert "No vehicles in inventory yet" in response.text


def test_logged_in_user_can_add_and_view_vehicle():
    register_and_login()

    add_response = client.post(
        "/vehicles/add",
        data={
            "make": "Toyota",
            "model": "Corolla",
            "year": "2021",
            "price": "18900",
            "color": "Silver",
            "mileage": "32000",
            "description": "Sample Sprint 1 vehicle",
        },
        follow_redirects=False,
    )

    assert add_response.status_code == 303

    list_response = client.get("/vehicles")
    assert list_response.status_code == 200
    assert "Toyota" in list_response.text
    assert "Corolla" in list_response.text

    detail_response = client.get("/vehicles/1")
    assert detail_response.status_code == 200
    assert "Sample Sprint 1 vehicle" in detail_response.text

    api_response = client.get("/api/vehicles/1")
    assert api_response.status_code == 200
    assert api_response.json()["make"] == "Toyota"


def test_vehicle_pages_require_login():
    response = client.get("/vehicles", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
