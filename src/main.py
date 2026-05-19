from pathlib import Path
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from starlette.middleware.sessions import SessionMiddleware

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = "sqlite:///./car_store.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True, nullable=False)
    model = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    color = Column(String, nullable=True)
    mileage = Column(Integer, nullable=True)
    description = Column(String, nullable=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Car Store Management System", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="change-this-secret-key-in-real-projects")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def find_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_logged_in_user(request: Request, db: Session) -> User | None:
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return db.query(User).filter(User.id == user_id).first()


def require_login(request: Request, db: Session) -> User | RedirectResponse:
    user = get_logged_in_user(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    return user


@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"user": get_logged_in_user(request, db)},
    )


@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        request,
        "register.html",
        {"user": None, "error": None},
    )


@app.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    if find_user_by_username(db, username):
        return templates.TemplateResponse(
            request,
            "register.html",
            {"user": None, "error": "Username already exists."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user = User(username=username, hashed_password=hash_password(password))
    db.add(user)
    db.commit()

    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"user": None, "error": None},
    )


@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = find_user_by_username(db, username)
    if user is None or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            request,
            "login.html",
            {"user": None, "error": "Invalid username or password."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    request.session["user_id"] = user.id
    return RedirectResponse(url="/vehicles", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/vehicles")
async def vehicle_list(request: Request, db: Session = Depends(get_db)):
    user = require_login(request, db)
    if isinstance(user, RedirectResponse):
        return user

    vehicles = db.query(Vehicle).order_by(Vehicle.id.desc()).all()
    return templates.TemplateResponse(
        request,
        "vehicles.html",
        {"user": user, "vehicles": vehicles},
    )


@app.get("/vehicles/add")
async def add_vehicle_page(request: Request, db: Session = Depends(get_db)):
    user = require_login(request, db)
    if isinstance(user, RedirectResponse):
        return user

    return templates.TemplateResponse(
        request,
        "add_vehicle.html",
        {"user": user},
    )


@app.post("/vehicles/add")
async def add_vehicle(
    request: Request,
    make: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    price: float = Form(...),
    color: str = Form(""),
    mileage: int = Form(0),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    user = require_login(request, db)
    if isinstance(user, RedirectResponse):
        return user

    vehicle = Vehicle(
        make=make,
        model=model,
        year=year,
        price=price,
        color=color,
        mileage=mileage,
        description=description,
    )
    db.add(vehicle)
    db.commit()

    return RedirectResponse(url="/vehicles", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/vehicles/{vehicle_id}")
async def vehicle_detail(vehicle_id: int, request: Request, db: Session = Depends(get_db)):
    user = require_login(request, db)
    if isinstance(user, RedirectResponse):
        return user

    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return templates.TemplateResponse(
        request,
        "vehicle_detail.html",
        {"user": user, "vehicle": vehicle},
    )


@app.get("/api/vehicles")
async def api_vehicle_list(db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).order_by(Vehicle.id.desc()).all()
    return [
        {
            "id": vehicle.id,
            "make": vehicle.make,
            "model": vehicle.model,
            "year": vehicle.year,
            "price": vehicle.price,
            "color": vehicle.color,
            "mileage": vehicle.mileage,
            "description": vehicle.description,
        }
        for vehicle in vehicles
    ]


@app.get("/api/vehicles/{vehicle_id}")
async def api_vehicle_detail(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return {
        "id": vehicle.id,
        "make": vehicle.make,
        "model": vehicle.model,
        "year": vehicle.year,
        "price": vehicle.price,
        "color": vehicle.color,
        "mileage": vehicle.mileage,
        "description": vehicle.description,
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)