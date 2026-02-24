from typing import Annotated, Annotated

from fastapi import APIRouter, Depends, Path, Query
from app.core.config import settings
from app.core.schemas import CombineOrgFilterPagination
from app.core.services import OrganizationService


router = APIRouter(tags=["Organizations"])

@router.get("/search", response_model=dict)
async def search_organizations(
    filter_and_pagination_query: Annotated[CombineOrgFilterPagination, Query()],
    service: OrganizationService = Depends(),
):
    return await service.search(
        filter_=filter_and_pagination_query,
    )
