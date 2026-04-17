import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/car_owners/{car_id}")
async def get_car_owner(car_id: int):
    owners = [
        {"id": 1, "name": "Ford", "owner": "Adam"},
        {"id": 2, "name": "BMW", "owner": "Pawel"},
        {"id": 3, "name": "Mercedes", "owner": "Ken"},
        {"id": 4, "name": "Renault", "owner": "Will"},
        {"id": 5, "name": "Tesla", "owner": "Steve"},
    ]
    for car in owners:
        if car["id"] == car_id:
            return car
    raise HTTPException(status_code=404, detail="Car not found")


@app.get("/car_places")
async def get_car_places(city: str | None = None):
    places = [
        {"id": 0, "name": "Ford", "color": "red", "place": "Gdańsk"},
        {"id": 1, "name": "BMW", "color": "blue", "place": "Łódź"},
        {"id": 2, "name": "Mercedes", "color": "green", "place": "Gdynia"},
        {"id": 3, "name": "Renault", "color": "silver", "place": "Sopot"},
        {"id": 4, "name": "Tesla", "color": "white", "place": "Sosnowiec"},
    ]
    if city is not None:
        return [c for c in places if c["place"].lower() == city.lower()]
    return places


@app.get("/car_prices")
async def get_car_prices():
    return [
        {"id": 0, "name": "Ford", "color": "red", "price": 100000, "currency": "PLN"},
        {"id": 1, "name": "BMW", "color": "blue", "price": 180000, "currency": "PLN"},
        {"id": 2, "name": "Mercedes", "color": "green", "price": 220000, "currency": "PLN"},
        {"id": 3, "name": "Renault", "color": "silver", "price": 95000, "currency": "PLN"},
        {"id": 4, "name": "Tesla", "color": "white", "price": 250000, "currency": "PLN"},
    ]


@app.get("/cars")
async def get_all_cars():
    return [
        {"id": 0, "name": "Ford", "color": "red"},
        {"id": 1, "name": "BMW", "color": "blue"},
        {"id": 2, "name": "Mercedes", "color": "green"},
        {"id": 3, "name": "Renault", "color": "silver"},
        {"id": 4, "name": "Tesla", "color": "white"},
    ]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)