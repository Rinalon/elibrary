from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.schemas import AuthorResponse, AuthorShortResponse, AuthorCreate
from db.crud import author_crud
from core.database import get_db

author_router = APIRouter()


@author_router.get("/", response_model=List[AuthorShortResponse], response_model_exclude_none=True)
async def get_all_authors(
        page: int = 1,
        size: int = 10,
        db: AsyncSession = Depends(get_db)
):
    """Получение всех авторов с разбиением по страницам"""
    authors = await author_crud.get_paginate(db = db, limit = size, offset = (page - 1) * size)

    if not authors:
        return []

    return authors

@author_router.get("/{author_id}", response_model=AuthorResponse, response_model_exclude_none=True)
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    """Получение конкретного автора"""
    author = await author_crud.get_by_id(db, author_id)
    if not author:
        raise HTTPException(404, "Author not found")

    return author

@author_router.post("/", response_model=AuthorResponse)
async def create_author(author_data: AuthorCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_author = await author_crud.create(db, author_data)
        return new_author
    except Exception as e:
        raise HTTPException(500, str(e))

