import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/car_owners")
async def get_car_owners():
    return [
        {"id": 1, "name": "Ford", "owner" : "Adam"},
        {"id": 2, "name": "BMW", "owner": "Pawel"},
        {"id": 3, "name": "Mercedes", "owner": "Ken"},
        {"id": 4, "name": "Renault", "owner": "Will"},
        {"id": 5, "name": "Tesla", "owner": "Steve"}
    ]



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

