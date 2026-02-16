import json
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import db_session

router = APIRouter(tags=["Building"])

@router.get("/find")
def find_building(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
):
    return {"message": "This is a placeholder for the building search endpoint."}

@router.post("/add")
def add_building(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
):
    return {"message": "This is a placeholder for the building addition endpoint."}

@router.post("/update")
def update_building(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
):
    return {"message": "This is a placeholder for the building update endpoint."}

@router.delete("/delete")
def delete_building(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
):
    return {"message": "This is a placeholder for the building deletion endpoint."}
