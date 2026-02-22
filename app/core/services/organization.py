from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.db.session import db_session
from app.core.repositories.organization import OrganizationRepository
from app.core.schemas import OrganizationOut, OrganizationFilter
from sqlalchemy.ext.asyncio import AsyncSession


class OrganizationService:
    def __init__(
        self,
        db: AsyncSession = Depends(db_session.session_getter),
    ):
        self.repo = OrganizationRepository(db)

    async def search(
        self,
        filter_: OrganizationFilter,
        page: int = 1,
        limit: int = 20,
        sort: Optional[str] = None,
    ) -> dict:
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