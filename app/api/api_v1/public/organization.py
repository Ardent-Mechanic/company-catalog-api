from typing import Annotated, Annotated, List, Optional

from fastapi import APIRouter, Body, Depends, Query
from app.core.config import settings
from app.core.schemas.organization import OrganizationFilter, OrganizationOut
from app.core.services import OrganizationService


router = APIRouter(tags=["Organizations"])

@router.get("/search", response_model=dict)
async def search_organizations(
    filter_query: OrganizationFilter = Depends(),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Optional[str] = Query(None, pattern="^(name|distance|rating|created_at)(:(asc|desc))?$"),
    service: OrganizationService = Depends(),
):
    # Здесь будет логика
    return await service.search(
        filter_=filter_query,
        page=page,
        limit=limit,
        sort=sort,
    )

