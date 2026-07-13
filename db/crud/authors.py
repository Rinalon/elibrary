from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from db.models import Author, Book

async def  get_authors_paginated(db: AsyncSession, limit: int = 10, offset: int = 0):
    """Функция для получения всех авторов с возможностью разбиения на страницы"""
    result = await db.execute(
        select(Author)
        .order_by(Author.author_name)
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()

async def get_author_by_id(db: AsyncSession, author_id: int):
    """Функция для получения конретного автора"""
    result = await db.execute(
        select(Author)
        .where(Author.author_id == author_id)
        .options(
            joinedload(Author.books).joinedload(Book.changeable)
        )
    )
    return result.unique().scalar_one_or_none()