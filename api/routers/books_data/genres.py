from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.schemas import GenreResponse, GenreShortResponse, GenreCreate
from db.crud import genre_crud
from core.database import get_db

genre_router = APIRouter()

@genre_router.get("/", response_model=List[GenreShortResponse], response_model_exclude_none=True)
async def get_all_genres(db: AsyncSession = Depends(get_db)):
    """Получение всех жанров"""
    genres = await genre_crud.get_all(db=db)

    if not genres:
        return []

    return genres

@genre_router.get("/{genre_id}",response_model=GenreResponse, response_model_exclude_none=True)
async def get_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    """Получение конкретного жанра"""
    genre = await genre_crud.get_by_id(db, genre_id)
    if not genre:
        raise HTTPException(404, "Genre not found")

    return genre

@genre_router.post("/", response_model=GenreResponse)
async def create_genre(data: GenreCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_genre = await genre_crud.create(db, data)
        return new_genre
    except Exception as e:
        raise HTTPException(500, str(e))