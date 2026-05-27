"""Pydantic schemas for request/response validation."""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ---------- Requests ----------

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------- Responses ----------

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2: allow ORM conversion


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: UserResponse


class VerifyResponse(BaseModel):
    """Response from GET /verify - used by other services."""
    valid: bool
    user_id: int
    email: EmailStr
    role: str


class ErrorResponse(BaseModel):
    detail: str
