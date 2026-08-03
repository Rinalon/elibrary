from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from db.models import Author, Book, BookChangeable
from db.schemas import AuthorCreate
from db.crud.base import BaseCRUD
from typing import Any, Optional, Tuple

class AuthorCRUD(BaseCRUD[Author, AuthorCreate]):
    async def get_by_id(
            self,
            db: AsyncSession,
            item_id: int,
            load_options: Optional[Tuple[Any]] = None
    ) -> Author | None:
        if not load_options:
            load_options = (
                selectinload(Author.books).joinedload(Book.changeable).load_only(BookChangeable.rating),
            )

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
