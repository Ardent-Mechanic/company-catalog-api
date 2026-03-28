from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.core.schemas import CombineOrgFilterPagination
from app.core.schemas.organization import OrganizationOut
from app.core.services import OrganizationService
from app.core.services import ActivityService

router = APIRouter(tags=["Activities"])


@router.get("/tree", response_model=dict)
async def find_all(
    service: ActivityService = Depends(),
):
    return await service.find_all_tree()