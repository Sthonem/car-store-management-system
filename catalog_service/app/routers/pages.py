"""
HTML pages (Jinja2 templates).
SCRUM-106: GET /vehicles - browse listing
SCRUM-107: GET /vehicles/{id} - detail page
SCRUM-101: GET /admin/add-vehicle - admin form
"""
from pathlib import Path
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.vehicle import Vehicle


templates_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


router = APIRouter(tags=["pages"])


@router.get("/vehicles", response_class=HTMLResponse, summary="Browse vehicle inventory")
def listing_page(request: Request, db: Session = Depends(get_db)):
    """
    SCRUM-106 ⭐ The customer-facing listing page.
    Public access, no authentication required.
    """
    vehicles = db.query(Vehicle).order_by(Vehicle.created_at.desc()).all()
    return templates.TemplateResponse(
        request, "listing.html", {"vehicles": vehicles}
    )


@router.get("/vehicles/{vehicle_id}", response_class=HTMLResponse, summary="Vehicle detail page")
def detail_page(vehicle_id: int, request: Request, db: Session = Depends(get_db)):
    """SCRUM-107 Detail page."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        return templates.TemplateResponse(
            request,
            "not_found.html",
            {"vehicle_id": vehicle_id},
            status_code=404,
        )
    return templates.TemplateResponse(
        request, "detail.html", {"vehicle": vehicle}
    )


@router.get(
    "/admin/add-vehicle",
    response_class=HTMLResponse,
    summary="Admin form to add a vehicle",
)
def add_vehicle_form(request: Request):
    """
    SCRUM-101 admin form.
    Note: Sprint 1 scope - the form expects the user to paste their JWT token.
    Sprint 2 will add proper admin login session cookie.
    """
    return templates.TemplateResponse(request, "add_vehicle.html", {})


@router.get("/login", response_class=HTMLResponse, summary="Login helper page")
def login_helper(request: Request):
    """A helper page that lets the user log in via Auth Service and copy the token."""
    return templates.TemplateResponse(request, "login.html", {})
