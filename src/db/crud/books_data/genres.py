from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.db.models import Genre, Book, BookChangeable
from src.db.models.books_data.genre import book_genre
from src.db.schemas import GenreCreate, GenreUpdate
from src.db.crud.base import BaseCRUD
from typing import Any, Optional, Tuple

class GenreCRUD(BaseCRUD[Genre, GenreCreate, GenreUpdate]):
    full_load_options: tuple = (
        selectinload(Genre.books).joinedload(Book.changeable).load_only(BookChangeable.rating),
    )
    async def get_by_id(
            self,
            db: AsyncSession,
            item_id: int,
            load_options: Optional[Tuple[Any]] = None
    ) -> Genre | None:
        load_options = load_options or self.full_load_options

        return await super().get_by_id(db, item_id, load_options)

    async def create(self, db: AsyncSession, data: GenreCreate):
        new_genre = Genre(
            title=data.title,
            description=data.description,
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

    async def update(
            self,
            db: AsyncSession,
            item_id: int,
            data: GenreUpdate,
            load_options: Optional[Tuple[Any]] = None,
    ) -> Genre | None:
        load_options = load_options or self.full_load_options

        if data.books:
            for book_id in data.books:
                await db.execute(
                    book_genre.insert().values(genre_id=item_id, book_id=book_id)
                )
            data.books = None

        return await super().update(db, item_id, data, load_options)