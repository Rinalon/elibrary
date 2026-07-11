from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from models import (
    Book,
    BookChangeable,
    Author,
    Genre,
    Publisher,
    Language,
    Review
)

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
