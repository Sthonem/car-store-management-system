"""
Vehicle JSON API endpoints.
SCRUM-101: POST /api/vehicles (admin add)
SCRUM-106: GET /api/vehicles (listing)
SCRUM-107: GET /api/vehicles/{id} (detail)
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth_client import get_current_user
from app.models.vehicle import Vehicle, VehicleStatus
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleListResponse


router = APIRouter(prefix="/api/vehicles", tags=["vehicles-api"])


@router.get(
    "",
    response_model=VehicleListResponse,
    summary="List vehicles (public)",
)
def list_vehicles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    SCRUM-106: Public listing of available vehicles with pagination.
    Sprint 2 will add search/filter/sort query parameters.
    """
    query = db.query(Vehicle)
    total = query.count()
    items = (
        query.order_by(Vehicle.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return VehicleListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=items,
    )


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
    summary="Get a single vehicle by ID (public)",
)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """SCRUM-107: Vehicle detail."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )
    return vehicle


@router.post(
    "",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new vehicle (authenticated)",
)
async def create_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),  # ← THIS calls Auth Service via REST
):
    """
    SCRUM-101: Admin adds a new vehicle to the inventory.

    The get_current_user dependency triggers a REST call to Auth Service's
    /verify endpoint - demonstrating the LA10 inter-service requirement.

    Sprint 1 scope: any authenticated user can add vehicles.
    Sprint 2 (SCRUM-85): tighten this to require role == "admin".
    """
    vehicle = Vehicle(
        brand=payload.brand,
        model=payload.model,
        year=payload.year,
        mileage=payload.mileage,
        price=payload.price,
        fuel_type=payload.fuel_type,
        status=VehicleStatus.available,
        description=payload.description,
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle
