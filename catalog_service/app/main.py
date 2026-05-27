"""
Catalog Service - Car Store Management System
Owns: vehicle inventory CRUD, listing page, detail page.
Calls Auth Service via REST for protected endpoints.
Port: 8002
"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.database import Base, engine
from app.routers import vehicles, pages, health

# Create tables on startup (Sprint 1 simple approach)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Car Store Catalog Service",
    description="Vehicle inventory and customer browsing service for Car Store Management System",
    version="1.0.0",
)

# Mount static files (CSS)
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.include_router(health.router)
app.include_router(pages.router)       # HTML pages (public)
app.include_router(vehicles.router)    # JSON API


@app.get("/")
def root():
    return {
        "service": "Car Store Catalog Service",
        "version": "1.0.0",
        "browse": "/vehicles",
        "docs": "/docs",
    }
