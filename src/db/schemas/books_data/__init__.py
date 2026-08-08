from src.db.schemas.books_data.books import (
    BookCreate,
    BookUpdate,
    BookResponse,
    BookFilter,
    BookShortResponse,
)

from src.db.schemas.books_data.reviews import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse
)

from src.db.schemas.books_data.dictionaries import (
    LanguageResponse,
    LanguageCreate,
    PublisherResponse,
    PublisherShortResponse,
    PublisherCreate,
    PublisherUpdate
)

from src.db.schemas.books_data.genres import (
    GenreResponse,
    GenreShortResponse,
    GenreCreate,
    GenreUpdate,
)

from src.db.schemas.books_data.authors import (
    AuthorShortResponse,
    AuthorResponse,
    AuthorCreate,
    AuthorUpdate,
)


BookResponse.model_rebuild()
AuthorResponse.model_rebuild()
GenreResponse.model_rebuild()
PublisherResponse.model_rebuild()

__all__ = [
    'BookCreate','BookUpdate', 'BookResponse', 'BookShortResponse',
    'BookFilter',
    'ReviewCreate', 'ReviewUpdate', 'ReviewResponse',
    'GenreResponse', 'GenreShortResponse', 'GenreCreate', 'GenreUpdate',
    'AuthorResponse', 'AuthorShortResponse', 'AuthorCreate', 'AuthorUpdate',
    'LanguageResponse', 'LanguageCreate',
    'PublisherResponse', 'PublisherShortResponse', 'PublisherCreate',
    'PublisherUpdate'
]

