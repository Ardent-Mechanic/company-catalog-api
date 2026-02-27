from typing import Optional
from unicodedata import name

from fastapi import Depends
from app.core.db.session import db_session
from app.core.exceptions.custom_exceptions import NotFoundError
from app.core.repositories.organization import OrganizationRepository
from app.core.schemas import OrganizationOut, CombineOrgFilterPagination
from sqlalchemy.ext.asyncio import AsyncSession


class OrganizationService:
    def __init__(
        self,
        db: AsyncSession = Depends(db_session.session_getter),
    ):
        self.repo = OrganizationRepository(db)

    async def search(
        self,
        filter_: CombineOrgFilterPagination,
    ) -> dict:
        
        page = filter_.page
        limit = filter_.limit
        sort = filter_.sort
        
        offset = (page - 1) * limit

        items, total = await self.repo.find_many(
            filter_, offset, limit, sort
        )

        return {
            "items": [OrganizationOut.model_validate(o) for o in items],
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit if total else 0,
        }


    async def search_by_id(self, org_id: int) -> OrganizationOut:
        org = await self.repo.find_by_id(org_id)
        if not org:
            raise NotFoundError(f"Organization with id {org_id} not found")
        return OrganizationOut.model_validate(org)
    

    async def find_by_name(self, name: str) -> dict:
        orgs, total = await self.repo.find_by_name(name)
        if not orgs:
            raise NotFoundError(f"Organization with name '{name}' not found")
    
        return {
            "items": [OrganizationOut.model_validate(o) for o in orgs],
            "total": total,
        }

    
    async def find_by_activity(self, activity_name: str) -> dict:
        orgs, total = await self.repo.find_by_activity(activity_name)
        if not orgs:
            raise NotFoundError(f"Organization with activity name '{activity_name}' not found")
    
        return {
            "items": [OrganizationOut.model_validate(o) for o in orgs],
            "total": total,
        }


    async def find_by_activity_depth(self, activity_name: str) -> dict:
        orgs, total = await self.repo.find_by_activity_depth(activity_name)
        if not orgs:
            raise NotFoundError(f"Organization with activity name '{activity_name}' not found")
    
        return {
            "items": [OrganizationOut.model_validate(o) for o in orgs],
            "total": total,
        }


    async def find_nearby(
        self,
        lat: float,
        lon: float,
        radius_km: float,
        limit: int = 20
    ) -> dict:
        radius_meters = radius_km * 1000  # Конвертация в метры
        orgs, total = await  self.repo.find_nearby( 
            lat=lat,
            lon=lon,
            radius_meters=radius_meters,
            limit=limit)


        if not orgs:
            raise NotFoundError(f"Organizations not found in radius {radius_km} km")

        return {
            "items": [OrganizationOut.model_validate(o) for o in orgs],
            "total": total,
        }
    

    async def find_in_square(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        limit: int = 20
    ) -> dict:
        orgs, total = await self.repo.find_in_square(
            lat1=lat1,
            lon1=lon1,
            lat2=lat2,
            lon2=lon2,
            limit=limit
        )

        if not orgs:
            raise NotFoundError(f"Organizations not found in the specified square")

        return {
            "items": [OrganizationOut.model_validate(o) for o in orgs],
            "total": total,
        }