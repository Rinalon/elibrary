from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from db.models import Author

async def  get_authors_paginated(db: AsyncSession, limit: int = 10, offset: int = 1):
    result = await db.execute(
        select(Author)
        .order_by(Author.author_name)
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()

async def get_author_by_id(db: AsyncSession, author_id: int):
    result = await db.execute(
        select(Author)
        .where(Author.author_id == author_id)
        .options(
            joinedload(Author.books)
        )
    )
    return result.unique().scalar_one_or_none()