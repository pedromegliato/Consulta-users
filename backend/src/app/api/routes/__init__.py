from fastapi import APIRouter

from app.api.routes import health, users

api_router = APIRouter(prefix="/api")
api_router.include_router(users.router)
api_router.include_router(health.router)

__all__ = ["api_router"]
