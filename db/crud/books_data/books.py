from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
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

async def  get_books_paginated(db: AsyncSession, limit: int = 10, offset: int = 0):
    """Функция для получения всех книг, разбитых по страницам"""
    result = await db.execute(
        select(Book)
        .join(Book.changeable)
        .options(joinedload(Book.changeable),
                 selectinload(Book.authors).load_only(Author.author_name))
        .order_by(desc(BookChangeable.rating))
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()

async def get_book_by_id(db: AsyncSession, book_id: int):
    """Функция для получения конретной книги, разбитых по страницам"""
    result = await db.execute(
        select(Book)
        .where(Book.book_id == book_id)
        .options(
            joinedload(Book.changeable),
            selectinload(Book.authors),
            selectinload(Book.genres),
            selectinload(Book.reviews).selectinload(Review.user).load_only(User.nickname),
            joinedload(Book.language),
            joinedload(Book.publisher).load_only(Publisher.name),
        )
    )
    return result.unique().scalar_one_or_none()

async def create_book(db: AsyncSession, book_data: BookCreate):
    """Функция для создания книги в базе"""
    new_book = Book(
        title=book_data.title,
        description=book_data.description,
        year_of_publish=book_data.year_of_publish,
        publisher_id=book_data.publisher_id,
        language_id=book_data.language_id,
        age_rating=book_data.age_rating,
        price=book_data.price,
        text_url=book_data.text_url,
        cover_url=book_data.cover_url
    )
    db.add(new_book)
    await db.flush()
    await db.refresh(new_book, attribute_names=["authors", "genres"])
    if book_data.author_ids:
        authors = await db.execute(
            select(Author).where(Author.author_id.in_(book_data.author_ids))
        )
        for author in authors.scalars().all():
            new_book.authors.append(author)

    if book_data.genre_ids:
        genres = await db.execute(
            select(Genre).where(Genre.genre_id.in_(book_data.genre_ids))
        )
        for genre in genres.scalars().all():
            new_book.genres.append(genre)

    await db.commit()

    await db.refresh(new_book)
    return new_book

