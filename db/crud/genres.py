from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from db.models import Genre

async def  get_genres(db: AsyncSession):
    result = await db.execute(select(Genre))
    return result.scalars().all()

async def get_genre_by_id(db: AsyncSession, genre_id: int):
    result = await db.execute(
        select(Genre)
        .where(Genre.genre_id == genre_id)
        .options(
            joinedload(Genre.books)
        )
    )
    return result.unique().scalar_one_or_none()