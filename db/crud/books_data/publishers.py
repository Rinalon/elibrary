from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from db.models import Publisher, Book


async def  get_publishers(db: AsyncSession):
    """Функция для получения всех жанров"""
    result = await db.execute(select(Publisher))
    return result.scalars().all()

async def get_publisher_by_id(db: AsyncSession, publisher_id: int):
    """Функция для получения конретного жанра"""
    result = await db.execute(
        select(Publisher)
        .where(Publisher.publisher_id == publisher_id)
        .options(
            joinedload(Publisher.books).joinedload(Book.changeable)
        )
    )
    return result.unique().scalar_one_or_none()