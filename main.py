import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/car_prices")
async def get_car_prices():
    return [
        {"id": 0, "name": "Ford", "color": "red", "price": "100000 zloti"},
        {"id": 1, "name": "BMW", "color": "blue", "price": "180000 zloti"},
        {"id": 2, "name": "Mercedes", "color": "green", "price": "220000 zloti"},
        {"id": 3, "name": "Renault", "color": "silver", "price": "95000 zloti"},
        {"id": 4, "name": "Tesla", "color": "white", "price": "250000 zloti"},
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)