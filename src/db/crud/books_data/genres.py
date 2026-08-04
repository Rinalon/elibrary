from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.db.models import Genre, Book, BookChangeable
from src.db.schemas import GenreCreate
from src.db.crud.base import BaseCRUD
from typing import Any, Optional, Tuple

class GenreCRUD(BaseCRUD[Genre, GenreCreate]):
    async def get_by_id(
            self,
            db: AsyncSession,
            item_id: int,
            load_options: Optional[Tuple[Any]] = None
    ) -> Genre | None:
        if load_options is None:
            load_options = (
                selectinload(Genre.books).joinedload(Book.changeable).load_only(BookChangeable.rating),
            )

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