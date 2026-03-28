from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.core.schemas import CombineOrgFilterPagination
from app.core.schemas.organization import OrganizationOut
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


@router.get("/nearby", response_model=dict)
async def find_nearby(
    lat: float = Query(..., description="Широта"),
    lon: float = Query(..., description="Долгота"),
    radius_km: float = Query(..., description="Радиус в километрах"),
    limit: int = 20,
    service: OrganizationService = Depends(),
):
    return await service.find_nearby(lat=lat, lon=lon, radius_km=radius_km, limit=limit)


@router.get("/in_square", response_model=dict)
async def find_in_square(
    lat1: float = Query(..., description="Широта верхнего левого угла"),
    lon1: float = Query(..., description="Долгота верхнего левого угла"),
    lat2: float = Query(..., description="Широта нижнего правого угла"),
    lon2: float = Query(..., description="Долгота нижнего правого угла"),
    limit: int = 20,
    service: OrganizationService = Depends(),
):
    return await service.find_in_square(lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2, limit=limit)


@router.get("/activity/{activity_name}", response_model=dict)
async def find_by_activity(
    activity_name: str = Path(..., description="Название деятельности"),
    service: OrganizationService = Depends(),
):
    return await service.find_by_activity(activity_name)


@router.get("/activity/depth/{activity_name}", response_model=dict)
async def find_by_activity_depth(
    activity_name: str = Path(..., description="Название деятельности"),
    service: OrganizationService = Depends(),
):
    return await service.find_by_activity_depth(activity_name)


@router.get("/name/{name}", response_model=dict)
async def search_by_name(
    name: str = Path(..., description="Имя организации"),
    service: OrganizationService = Depends(),
):
    return await service.find_by_name(name)


@router.get("/{org_id}", response_model=OrganizationOut)
async def search_by_id(
    org_id: int = Path(...),
    service: OrganizationService = Depends(),
):
    return await service.search_by_id(org_id)
