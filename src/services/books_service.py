from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from crud.books import get_book_by_id
from schemas import (
    BookResponse,
)

async def get_book_page(db: AsyncSession, book_data):
    pass