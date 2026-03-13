import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/carPlaces")
async def get_car_places():
    return [
        {"id": 0, "name": "Ford", "color": "red", "place": "Gdańsk"},
        {"id": 1, "name": "BMW", "color": "blue", "place": "Łódź"},
        {"id": 2, "name": "Mercedes", "color": "green", "place": "Gdynia"},
        {"id": 3, "name": "Renault", "color": "silver", "place": "Sopot"},
        {"id": 4, "name": "Tesla", "color": "white", "place": "Sosnowiec"},
    ]

if __name__ == "_main_":
    uvicorn.run(app, host="0.0.0.0", port=8000)