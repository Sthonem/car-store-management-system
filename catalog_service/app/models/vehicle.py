"""
Vehicle model.
Implements SCRUM-109 + subtasks SCRUM-147, 149.
"""
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, Enum, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class FuelType(str, enum.Enum):
    gasoline = "gasoline"
    diesel = "diesel"
    electric = "electric"
    hybrid = "hybrid"


class VehicleStatus(str, enum.Enum):
    available = "available"
    sold = "sold"
    reserved = "reserved"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50), nullable=False, index=True)
    model = Column(String(50), nullable=False, index=True)
    year = Column(Integer, nullable=False)
    mileage = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)  # Decimal for money
    fuel_type = Column(Enum(FuelType), nullable=False)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.available, nullable=False)
    description = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
