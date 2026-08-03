from sqlalchemy import select, desc, ClauseElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from typing import Any, List, Optional, Tuple
from db.crud.base import BaseCRUD, ModelType
from db.models import (
    Book,
    BookChangeable,
    Review,
    Author,
    Genre,
    User,
    Publisher
)
from db.schemas import BookCreate

class BookCRUD(BaseCRUD[Book, BookCreate]):
    async def get_paginate(
            self,
            db: AsyncSession,
            limit: int = 10,
            offset: int = 0,
            order: Optional[Tuple[ClauseElement]] = None,
            load_options: Optional[Tuple[Any]] = None,
    ) -> List[ModelType]:
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
            *load_options: Any
    ) -> Book | None:
        if not load_options:
            load_options = (
                joinedload(Book.changeable),
                selectinload(Book.authors),
                selectinload(Book.genres),
                selectinload(Book.reviews).selectinload(Review.user).load_only(User.nickname),
                joinedload(Book.language),
                joinedload(Book.publisher).load_only(Publisher.name),
            )

        return await super().get_by_id(db, item_id, *load_options)

    async def create(self, db: AsyncSession, data: BookCreate) -> Book:
        book_data = data.model_dump(exclude={"author_ids", "genre_ids"})
        new_book = Book(**book_data)
        db.add(new_book)
        await db.flush()

        if data.author_ids:
            authors = await db.execute(
                select(Author).where(Author.author_id.in_(data.author_ids))
            )
            new_book.authors.extend(authors.scalars().all())

        if data.genre_ids:
            genres = await db.execute(
                select(Genre).where(Genre.genre_id.in_(data.genre_ids))
            )
            new_book.genres.extend(genres.scalars().all())

        await db.commit()
        await db.refresh(new_book)
        return new_book

