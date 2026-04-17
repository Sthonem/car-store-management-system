from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Basic example test (required for 1p)
def test_example():
    assert True


# Three tests

def test_get_car_owner_by_id():
    """Change 1: /car_owners/{car_id} should return a single owner by path parameter."""
    response = client.get("/car_owners/2")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "BMW"
    assert data["owner"] == "Pawel"


def test_get_car_owner_not_found():
    """Change 1 (extra): non-existent id should return 404."""
    response = client.get("/car_owners/999")
    assert response.status_code == 404


def test_car_places_city_filter():
    """Change 2: /car_places?city= should filter results by city."""
    response = client.get("/car_places?city=Gdańsk")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Ford"


def test_car_prices_are_integers():
    """Change 3: /car_prices must return integer prices and a currency field."""
    response = client.get("/car_prices")
    assert response.status_code == 200
    data = response.json()
    for car in data:
        assert isinstance(car["price"], int)
        assert car["currency"] == "PLN"