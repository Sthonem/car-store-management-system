"""
Auth client - REST call to Auth Service for token verification.

THIS IS THE CORE OF THE LA10 REQUIREMENT:
"two services that interchange communication with each other via REST calls"

When a protected endpoint receives a request, this module calls Auth Service's
/verify endpoint via HTTP. Auth Service is the single source of truth for
token validity.
"""
import httpx
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings


security = HTTPBearer()


async def verify_token_with_auth_service(token: str) -> dict:
    """
    Call Auth Service's /verify endpoint over REST.
    Returns user info dict on success, raises HTTPException on failure.
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{settings.auth_service_url}/verify",
                headers={"Authorization": f"Bearer {token}"},
            )
    except httpx.RequestError as e:
        # Auth service is unreachable - infrastructure failure
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Auth service unavailable: {str(e)}",
        )

    if response.status_code != 200:
        # Token was rejected by Auth - propagate the rejection
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return response.json()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    FastAPI dependency that protects an endpoint.
    Usage:
        @router.post("/api/vehicles")
        def create_vehicle(user: dict = Depends(get_current_user)):
            ...

    The user dict contains: user_id, email, role.
    """
    return await verify_token_with_auth_service(credentials.credentials)
