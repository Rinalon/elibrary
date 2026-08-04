from sqlalchemy import select, desc, ClauseElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from typing import Any, List, Optional, Tuple
from src.db.crud.base import BaseCRUD, ModelType
from src.db.models import (
    Book,
    BookChangeable,
    Review,
    Author,
    User,
    Publisher, Language,
)
from src.db.models.books_data.author import author_book
from src.db.models.books_data.genre import book_genre
from src.db.schemas import BookCreate, BookUpdate

class BookCRUD(BaseCRUD[Book, BookCreate, BookUpdate]):
    full_load_options: tuple = (
        joinedload(Book.changeable),
        selectinload(Book.authors),
        selectinload(Book.genres),
        selectinload(Book.reviews).selectinload(Review.user).load_only(User.nickname),
        joinedload(Book.language).load_only(Language.title),
        joinedload(Book.publisher).load_only(Publisher.name),
    )

    async def get_paginate(
            self,
            db: AsyncSession,
            limit: int = 10,
            offset: int = 0,
            order: Optional[Tuple[ClauseElement]] = None,
            load_options: Optional[Tuple[Any]] = None,
    ) -> List[Book]:
        if order is None:
            order = (desc(BookChangeable.rating),)

        if load_options is None:
            load_options = (
                joinedload(Book.changeable).load_only(BookChangeable.rating, BookChangeable.watched),
                selectinload(Book.authors).load_only(Author.author_name),
            )

        query = (
            select(Book)
            .join(BookChangeable, Book.book_id == BookChangeable.book_id)
            .limit(limit)
            .offset(offset)
        )

        for cond in order:
            query = query.order_by(cond)

        for option in load_options:
            query = query.options(option)

        result = await db.execute(query)
        return result.unique().scalars().all()

    async def get_by_id(
            self,
            db: AsyncSession,
            item_id: int,
            load_options: Optional[Tuple[Any]] = None
    ) -> Book | None:
        load_options = load_options or self.full_load_options

        return await super().get_by_id(db, item_id, load_options)


    async def create(self, db: AsyncSession, data: BookCreate) -> Book:
        book_data = data.model_dump(exclude={"author_ids", "genre_ids"})
        new_book = Book(**book_data)
        db.add(new_book)
        await db.flush()

        db.add(BookChangeable(book_id=new_book.book_id))

        for author_id in data.author_ids:
            await db.execute(
                author_book.insert().values(author_id=author_id, book_id=new_book.book_id)
            )

        for genre_id in data.genre_ids:
            await db.execute(
                book_genre.insert().values(genre_id=genre_id, book_id=new_book.book_id)
            )

        await db.commit()
        return await self.get_by_id(db, new_book.book_id)

    async def update(
            self,
            db: AsyncSession,
            item_id: int,
            data: BookUpdate,
            load_options: Optional[Tuple[Any]] = None,
    ) -> Book | None:
        load_options = load_options or self.full_load_options

        extra_fields = ["genre_ids", "author_ids"]
        if data.author_ids:
            for author_id in data.author_ids:
                await db.execute(
                    author_book.insert().values(author_id=author_id, book_id=item_id)
                )
            data.author_ids = None

        if data.genre_ids:
            for genre_id in data.genre_ids:
                await db.execute(
                    book_genre.insert().values(genre_id=genre_id, book_id=item_id)
                )
            data.genre_ids = None

        return await super().update(db, item_id, data, load_options)