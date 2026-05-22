"""Pydantic schemas for Vehicle validation."""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from app.models.vehicle import FuelType, VehicleStatus


CURRENT_YEAR = date.today().year


class VehicleCreate(BaseModel):
    brand: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=1990, le=CURRENT_YEAR + 1)
    mileage: int = Field(..., ge=0)
    price: Decimal = Field(..., gt=0)
    fuel_type: FuelType

    @field_validator("brand", "model")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class VehicleResponse(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    mileage: int
    price: Decimal
    fuel_type: FuelType
    status: VehicleStatus
    created_at: datetime

    class Config:
        from_attributes = True


class VehicleListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[VehicleResponse]
