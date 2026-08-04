from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.db.models import Author, Book, BookChangeable
from src.db.schemas import AuthorCreate, AuthorUpdate
from src.db.crud.base import BaseCRUD
from src.db.models.books_data.author import author_book
from typing import Any, Optional, Tuple

class AuthorCRUD(BaseCRUD[Author, AuthorCreate, AuthorUpdate]):
    full_load_options: tuple = (
                selectinload(Author.books).joinedload(Book.changeable).load_only(BookChangeable.rating),
    )

    async def get_by_id(
            self,
            db: AsyncSession,
            item_id: int,
            load_options: Optional[Tuple[Any]] = None
    ) -> Author | None:
        load_options = load_options or self.full_load_options

        return await super().get_by_id(db, item_id, load_options)

    async def create(self, db: AsyncSession, data: AuthorCreate):
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

    async def update(
            self,
            db: AsyncSession,
            item_id: int,
            data: AuthorUpdate,
            load_options: Optional[Tuple[Any]] = None,
    ) -> Author | None:
        load_options = load_options or self.full_load_options

        if data.books:
            for book_id in data.books:
                await db.execute(
                    author_book.insert().values(author_id=item_id, book_id=book_id)
                )
            data.books = None

        return await super().update(db, item_id, data, load_options)