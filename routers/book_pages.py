from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schemas import BookResponse, AuthorResponse, GenreResponse, ReviewResponse
from crud.books import get_book_by_id
from core.database import get_db

books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    print(f"🔍 Ищем книгу с ID: {book_id}, тип: {type(book_id)}")
    # 1. Получаем SQLAlchemy-объект Book (с уже подгруженными авторами и жанрами)
    db_book = await get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(404, "Book not found")

    # 2. FastAPI сам превратит db_book в BookResponse
    #    Pydantic увидит db_book.authors и db_book.genres
    #    и рекурсивно применит AuthorResponse и GenreResponse
    return db_book