from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.schemas import BookResponse, BookShortResponse
from db.crud.books import get_book_by_id, get_books_paginated
from core.database import get_db

books_router = APIRouter(prefix="/books", tags=["books"])

@books_router.get("/", response_model=List[BookShortResponse], response_model_exclude_none=True)
async def get_all_books(
        page: int = 1,
        size: int = 10,
        db: AsyncSession = Depends(get_db)
):
    """Получение всех книг с разбиением по страницам"""
    books = await get_books_paginated(db=db, limit=size, offset= (page - 1) * size)

    if not books:
        return []

    return books

@books_router.get("/{book_id}", response_model=BookResponse, response_model_exclude_none=True)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """Получение конкретной книги с разбиением по страницам"""
    book = await get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(404, "Book not found")

    return book
