import logging
from typing import Optional, Sequence

from geoalchemy2 import Geography
from geoalchemy2.functions import ST_Distance, ST_DWithin
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, with_expression

from app.core.models import Activity, Building, Organization
from app.core.schemas import OrganizationFilter


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
            where_clauses.append(Organization.activities.any(Activity.id == filter_.activity_id))

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
        # elif sort_by == "distance":

        # Подсчёт общего количества
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.db.scalar(count_stmt) or 0

        # Пагинация
        stmt = stmt.offset(offset).limit(limit)

        result = await self.db.scalars(stmt)
        items = result.all()  # List[Organization]

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

    async def find_by_name(self, name: str) -> tuple[Sequence[Organization], int]:
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.building),
                selectinload(Organization.phone_numbers),
            )
            .where(Organization.name.ilike(f"%{name}%"))
        )

        result = await self.db.scalars(stmt)
        items = result.all()
        return items, len(items)

    async def find_by_activity(self, activity_name: str) -> tuple[Sequence[Organization], int]:
        stmt = (
            select(Organization)
            .join(Organization.activities)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.building),
                selectinload(Organization.phone_numbers),
            )
            .where(Activity.name.ilike(f"%{activity_name}%"))
        )

        result = await self.db.scalars(stmt)
        items = result.all()
        return items, len(items)

    async def find_by_activity_depth(
        self, activity_name: str
    ) -> tuple[Sequence[Organization], int]:
        cte = (
            select(Activity.id)
            .where(Activity.name.ilike(f"%{activity_name}%"))
            .cte(recursive=True, name="activity_tree")
        )
        # Рекурсивная часть
        cte = cte.union(select(Activity.id).where(Activity.parent_id == cte.c.id))

        # Основной запрос организации по id из CTE
        stmt = (
            select(Organization)
            .join(Organization.activities)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.building),
                selectinload(Organization.phone_numbers),
            )
            .where(Activity.id.in_(select(cte.c.id)))
            .distinct()
        )

        result = await self.db.scalars(stmt)
        items = result.all()
        return items, len(items)

    async def find_nearby(
        self,
        lat: float,
        lon: float,
        radius_meters: float = 100,
        limit: int = 20,
    ) -> tuple[Sequence[Organization], int]:
        point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)

        distance_expr = ST_Distance(Building.geom, point.cast(Geography)).label("distance")

        stmt = (
            select(Organization)
            .join(Building)
            .where(ST_DWithin(Building.geom, point, radius_meters))
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.building),
                selectinload(Organization.phone_numbers),
                # добавляем в запрос расстояние, чтобы оно было доступно в результатах
                with_expression(Organization.distance, distance_expr),
            )
            .order_by(distance_expr)
            .limit(limit)
        )

        result = await self.db.scalars(stmt)
        organizations = result.all()

        # Теперь у каждого объекта уже есть .distance
        # и это настоящие экземпляры Organization
        return organizations, len(organizations)

    async def find_in_square(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        limit: int = 20,
    ) -> tuple[Sequence[Organization], int]:
        stmt = (
            select(Organization)
            .join(Building, Organization.building_id == Building.id)
            .where(
                # ST_Within проверяет, находится ли точка внутри прямоугольника
                # Или используем && (пересечение bounding box) для индекса
                Building.geom.bool_op("&&")(
                    func.ST_SetSRID(func.ST_MakeEnvelope(lon1, lat1, lon2, lat2), 4326)
                )
            )
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.building),
                selectinload(Organization.phone_numbers),
            )
            .limit(limit)
        )

        result = await self.db.scalars(stmt)
        organizations = result.all()
        return organizations, len(organizations)
