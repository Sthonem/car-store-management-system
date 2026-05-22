"""
Auth endpoints: /register, /login, /verify, /me.
Implements SCRUM-86 (register/login) and SCRUM-88 (token verification).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.security import hash_password, verify_password
from app.core.jwt_handler import create_access_token, decode_access_token
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    TokenResponse,
    VerifyResponse,
)

router = APIRouter(prefix="", tags=["auth"])
security = HTTPBearer()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new customer account",
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    SCRUM-86 / SCRUM-90: Register endpoint.
    - Validates email and password length
    - Hashes password with bcrypt
    - Persists user with default role "customer"
    """
    # Check duplicate email
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="customer",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate and receive a JWT",
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    SCRUM-86 / SCRUM-91: Login endpoint.
    - Verifies password using bcrypt
    - Issues JWT on success
    - Returns 401 on invalid credentials
    """
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user_id=user.id, email=user.email, role=user.role)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=settings.jwt_expiry_minutes * 60,
        user=UserResponse.model_validate(user),
    )


@router.get(
    "/verify",
    response_model=VerifyResponse,
    summary="Validate a token (called by other services)",
)
def verify(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    SCRUM-88 / SCRUM-103: Token verification endpoint.
    Called by Catalog Service over REST to validate Bearer tokens.
    Returns 401 if token is invalid, expired, or refers to a deleted user.
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = int(payload["sub"])
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
        )

    return VerifyResponse(
        valid=True,
        user_id=user.id,
        email=user.email,
        role=user.role,
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get the current user's profile",
)
def me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """Returns the profile of the currently logged-in user."""
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
