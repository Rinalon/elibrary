from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.schemas import BookResponse, BookShortResponse, BookCreate
from db.crud import get_book_by_id, get_books_paginated, create_book
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

@books_router.post("/", )
async def create_new_book(book_data: BookCreate, db: AsyncSession = Depends(get_db)):
    """Создать новую книгу."""
    try:
        new_book = await create_book(db, book_data)
        return new_book
    except IntegrityError as e:
        raise HTTPException(409, detail="Book already exists")
    except Exception as e:
        raise HTTPException(500, detail=str(e))