from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.schemas import PublisherResponse, PublisherShortResponse
from db.crud import get_publisher_by_id, get_publishers
from core.database import get_db

publisher_router = APIRouter(prefix="/publishers", tags=["publishers"])

@publisher_router.get("/", response_model=List[PublisherShortResponse], response_model_exclude_none=True)
async def get_all_publishers(db: AsyncSession = Depends(get_db)):
    """Получение всех издателей"""
    publishers = await get_publishers(db=db)

    if not publishers:
        return []

    return publishers

@publisher_router.get("/{publisher_id}", response_model=PublisherResponse, response_model_exclude_none=True)
async def get_publisher(publisher_id: int, db: AsyncSession = Depends(get_db)):
    """Получение конкретного издателя"""
    publisher = await get_publisher_by_id(db, publisher_id)
    if not publisher:
        raise HTTPException(404, "Publisher not found")

    return publisher