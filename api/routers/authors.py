from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.schemas import AuthorResponse, AuthorShortResponse
from db.crud.authors import get_author_by_id, get_authors_paginated
from core.database import get_db

author_router = APIRouter(prefix="/authors", tags=["authors"])

@author_router.get("/", response_model=List[AuthorShortResponse], response_model_exclude_none=True)
async def get_all_authors(
        page: int = 1,
        size: int = 10,
        db: AsyncSession = Depends(get_db)
):
    """Получение всех авторов с разбиением по страницам"""
    authors = await get_authors_paginated(db = db, limit = size, offset = (page - 1) * size)

    if not authors:
        return []

    return authors

@author_router.get("/{author_id}", response_model=AuthorResponse, response_model_exclude_none=True)
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    """Получение конкретного автора"""
    author = await get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(404, "Author not found")

    return author