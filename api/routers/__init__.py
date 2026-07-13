from api.routers.books import books_router
from api.routers.authors import author_router
from api.routers.genres import genre_router
from api.routers.publishers import publisher_router

__all__ = [
    'books_router',
    'author_router',
    'genre_router',
    'publisher_router',
]