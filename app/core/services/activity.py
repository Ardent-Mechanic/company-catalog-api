from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import db_session
from app.core.exceptions.custom_exceptions import NotFoundError
from app.core.repositories.activity import ActivityRepository
from app.core.schemas import ActivityTree


class ActivityService:
    def __init__(
        self,
        db: AsyncSession = Depends(db_session.session_getter),
    ):
        self.repo = ActivityRepository(db)

    async def find_all_tree(
        self,
    ) -> dict:

        items = await self.repo.test()

        if not items:
            raise NotFoundError("No activities found")

        return {
            "items": [ActivityTree.model_validate(o) for o in items],
        }