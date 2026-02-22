from fastapi import APIRouter

from .organization import router as organization_router
from app.core.config import settings

router = APIRouter()

# all public routers
router.include_router(organization_router, prefix=settings.api.v1.organizations)