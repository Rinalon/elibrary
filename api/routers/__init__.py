from fastapi import APIRouter

from api.routers.books_data import books_data_router

routers = APIRouter()
routers.include_router(books_data_router)

__all__ = [
    'routers'
]