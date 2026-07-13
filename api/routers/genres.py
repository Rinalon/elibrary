from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.schemas import GenreResponse, GenreShortResponse
from db.crud.genres import get_genre_by_id, get_genres
from core.database import get_db

genre_router = APIRouter(prefix="/genres", tags=["genres"])

@genre_router.get("/", response_model=List[GenreShortResponse], response_model_exclude_none=True)
async def get_all_genres(db: AsyncSession = Depends(get_db)):
    """Получение всех жанров"""
    genres = await get_genres(db=db)

    if not genres:
        return []

    return genres

@genre_router .get("/{genre_id}",response_model=GenreResponse, response_model_exclude_none=True)
async def get_genre(book_id: int, db: AsyncSession = Depends(get_db)):
    """Получение конкретного жанра"""
    genre = await get_genre_by_id(db, book_id)
    if not genre:
        raise HTTPException(404, "Genre not found")

    return genre