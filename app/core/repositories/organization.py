import logging

from sqlalchemy import Tuple, func, select, and_, or_
from sqlalchemy.orm import Session, selectinload
from typing import Optional, List, Sequence, Sequence

from app.core.models import Organization, Activity, Building, PhoneNumber
from app.core.schemas import OrganizationFilter

from sqlalchemy.ext.asyncio import AsyncSession

class OrganizationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_many(
        self,
        filter_: OrganizationFilter,
        offset: int = 0,
        limit: int = 20,
        sort_by: Optional[str] = None,
    ) -> tuple[Sequence[Organization], int]:
        # Базовый запрос с eager loading
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.building),
                selectinload(Organization.phone_numbers),
            )
            .distinct()
        )

        # Динамические условия
        where_clauses = []

        if filter_.q:
            where_clauses.append(Organization.name.ilike(f"%{filter_.q}%"))

        if filter_.activity_id:
            where_clauses.append(
                Organization.activities.any(Activity.id == filter_.activity_id)
            )

        if filter_.activity_ids:
            where_clauses.append(
                Organization.activities.any(Activity.id.in_(filter_.activity_ids))
            )

        if filter_.building_id:
            where_clauses.append(Organization.building_id == filter_.building_id)

        if filter_.min_lat is not None and filter_.max_lat is not None:
            where_clauses.append(
                and_(
                    Building.latitude >= filter_.min_lat,
                    Building.latitude <= filter_.max_lat,
                    Building.longitude >= filter_.min_lon,
                    Building.longitude <= filter_.max_lon,
                )
            )

        if where_clauses:
            stmt = stmt.where(and_(*where_clauses))

        # Сортировка
        if sort_by == "name":
            stmt = stmt.order_by(Organization.name.asc())
        # elif sort_by == "distance":  # позже добавим haversine или PostGIS

        # Подсчёт общего количества 
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.db.scalar(count_stmt) or 0

        # Пагинация
        stmt = stmt.offset(offset).limit(limit)

        result = await self.db.scalars(stmt)
        items = result.all() # List[Organization]

        logging.info(f"Found {(len(items))} organizations (total: {total}) with filter: {filter_}")

        return items, total
    
    async def find_by_id(self, org_id: int) -> Optional[Organization]:
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.building),
                selectinload(Organization.phone_numbers),
            )
            .where(Organization.id == org_id)
        )

        result = await self.db.scalar(stmt)
        return result