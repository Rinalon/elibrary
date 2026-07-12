from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.schemas import BookResponse
from db.crud.books import get_book_by_id
from core.database import get_db

books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    db_book = await get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(404, "Book not found")

    return db_book