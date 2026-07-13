from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from db.models import Genre, Book


async def get_genres(db: AsyncSession):
    """Функция для получения всех жанров"""
    result = await db.execute(select(Genre))
    return result.scalars().all()

async def get_genre_by_id(db: AsyncSession, genre_id: int):
    """Функция для получения конретного жанра"""
    result = await db.execute(
        select(Genre)
        .where(Genre.genre_id == genre_id)
        .options(
            joinedload(Genre.books).joinedload(Book.changeable),
        )
    )
    return result.unique().scalar_one_or_none()