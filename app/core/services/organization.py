from typing import Optional

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