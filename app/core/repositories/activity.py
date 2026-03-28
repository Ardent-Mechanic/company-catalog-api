from typing import Sequence

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, with_expression

from app.core.models import Activity
from app.core.schemas.activity import ActivityTree


class ActivityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_all_tree(
        self,
    ) -> tuple[Sequence[Activity], int]:
        # Получаем все активности с их дочерними элементами
        stmt = (
            select(Activity)
            .options(selectinload(Activity.children))
            .where(Activity.parent_id == None)  # Получаем только корневые элементы
        )
        result = await self.db.execute(stmt)
        items = result.scalars().all()

        # Получаем общее количество корневых элементов
        count_stmt = select(func.count()).where(Activity.parent_id == None)
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar_one()

        return items, total
    

    async def test(
        self
    ) -> list[dict]:
        stmt = select(Activity)
        result = await self.db.execute(stmt)
        activities = result.scalars().all()

        # создаём словарь для будущего дерева
        tree_map = {
            a.id: {
                "id": a.id,
                "name": a.name,
                "parent_id": a.parent_id,
                "organization_count": getattr(a, "organization_count", 0),
                "children": [],
            }
            for a in activities
        }

        root_nodes = []

        for a in activities:
            node = tree_map[a.id]

            if a.parent_id:
                parent_node = tree_map[a.parent_id]
                parent_node["children"].append(node)
            else:
                root_nodes.append(node)

        return root_nodes