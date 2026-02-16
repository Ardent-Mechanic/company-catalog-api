from fastapi import APIRouter
from app.core.config import settings


from .public import router as public_router

router = APIRouter(prefix=settings.api.v1.prefix)

# public endpoints
router.include_router(public_router)
# protected endpoints
# router.include_router(protected_router)