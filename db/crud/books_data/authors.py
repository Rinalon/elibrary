from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from db.models import Author, Book
from db.schemas import AuthorCreate


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
            selectinload(Author.books).joinedload(Book.changeable)
        )
    )
    return result.unique().scalar_one_or_none()

async def create_author(db: AsyncSession, data: AuthorCreate):
    new_author = Author(
        author_name=data.author_name,
        author_info=data.author_info
    )
    db.add(new_author)
    await db.flush()

    if data.books:
        books = await db.execute(
            select(Book).where(Book.book_id.in_(data.books))
        )
        for book in books.scalars().all():
            new_author.books.append(book)

    await db.commit()
    await db.refresh(new_author)
    return new_author
