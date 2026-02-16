from fastapi import APIRouter

from .building import router as user_router
from app.core.config import settings

router = APIRouter()

# all public routers
router.include_router(user_router, prefix=settings.api.v1.building)