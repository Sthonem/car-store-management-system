"""Health check endpoint for docker-compose healthchecks."""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "auth_service"}
