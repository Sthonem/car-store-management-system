"""
Auth Service - Car Store Management System
Owns: user registration, login, JWT issuing/verification.
Port: 8001
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers import auth, health

# Create tables on startup (Sprint 1: simple; production would use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Car Store Auth Service",
    description="Authentication and authorization service for Car Store Management System",
    version="1.0.0",
)

# CORS: allow catalog_service to call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {
        "service": "Car Store Auth Service",
        "version": "1.0.0",
        "docs": "/docs",
    }
