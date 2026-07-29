from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from db.models import Genre, Book
from db.schemas import GenreCreate


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

async def create_genre(db: AsyncSession, data: GenreCreate):
    new_genre = Genre(
        title = data.title,
        description = data.description,
    )
    db.add(new_genre)
    await db.flush()

    if data.books:
        books = await db.execute(
            select(Book).where(Book.book_id.in_(data.books))
        )

        for book in books.scalars().all():
            new_genre.books.append(book)

    await db.commit()
    await db.refresh(new_genre)
    return new_genre