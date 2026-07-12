from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from db.models import Book, BookChangeable, Review

async def  get_books_paginated(db: AsyncSession, limit: int = 10, offset: int = 1):
    result = await db.execute(
        select(Book)
        .join(Book.changeable)
        .options(selectinload(Book.changeable), selectinload(Book.authors))
        .order_by(desc(BookChangeable.rating))
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()

async def get_book_by_id(db: AsyncSession, book_id: int):
    result = await db.execute(
        select(Book)
        .where(Book.book_id == book_id)
        .options(
            joinedload(Book.changeable),
            joinedload(Book.authors),
            joinedload(Book.genres),
            selectinload(Book.reviews).selectinload(Review.user),
        )
    )
    return result.unique().scalar_one_or_none()