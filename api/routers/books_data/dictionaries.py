from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.crud import language_crud, publisher_crud
from db.schemas import (
    PublisherResponse,
    PublisherShortResponse,
    PublisherCreate,
    LanguageResponse,
    LanguageCreate
)

from core.database import get_db

language_router = APIRouter()
@language_router.get("/", response_model=List[LanguageResponse])
async def get_languages(db: AsyncSession = Depends(get_db)):
    return await language_crud.get_all(db)

@language_router.post("/", response_model=LanguageResponse)
async def create_language(data: LanguageCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_language = await language_crud.create(db, data)
        return new_language
    except Exception as e:
        raise HTTPException(500, str(e))

publisher_router = APIRouter()

@publisher_router.get("/", response_model=List[PublisherShortResponse], response_model_exclude_none=True)
async def get_all_publishers(db: AsyncSession = Depends(get_db)):
    return await publisher_crud.get_all(db)

@publisher_router.get("/{publisher_id}", response_model=PublisherResponse, response_model_exclude_none=True)
async def get_publisher(publisher_id: int, db: AsyncSession = Depends(get_db)):
    return await publisher_crud.get_by_id(publisher_id, db)

@publisher_router.post("/", response_model=PublisherResponse)
async def create_publisher(publisher: PublisherCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_publisher = await publisher_crud.create(db, publisher)
        return new_publisher
    except Exception as e:
        raise HTTPException(500, str(e))