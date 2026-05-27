"""
JWT token creation and validation.
Implements SCRUM-88 subtasks: SCRUM-103 Session Control & Lifecycle,
SCRUM-104 Handle expired/invalid token responses.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(user_id: int, email: str, role: str = "customer") -> str:
    """
    Create a JWT access token for the given user.
    Returns the encoded token string.
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.jwt_expiry_minutes)

    payload = {
        "sub": str(user_id),       # subject = user id (string per JWT spec)
        "email": email,
        "role": role,
        "exp": expire,              # expiration
        "iat": now,                 # issued at
    }

    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT.
    Returns the payload dict if valid, None if invalid/expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        # Includes ExpiredSignatureError, JWSError, etc.
        return None
