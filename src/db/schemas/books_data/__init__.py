from src.db.schemas.books_data.books import (
    BookCreate,
    BookResponse,
    BookShortResponse,
    BookUpdate,
    BookFilter,
)

from src.db.schemas.books_data.reviews import (
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate,
)

from src.db.schemas.books_data.publisher import (
    PublisherCreate,
    PublisherResponse,
    PublisherShortResponse,
    PublisherUpdate
)

from src.db.schemas.books_data.language import (
    LanguageCreate,
    LanguageResponse,
    LanguageUpdate
)

from src.db.schemas.books_data.genres import (
    GenreCreate,
    GenreResponse,
    GenreShortResponse,
    GenreUpdate,
)

from src.db.schemas.books_data.authors import (
    AuthorCreate,
    AuthorResponse,
    AuthorShortResponse,
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
    'LanguageResponse', 'LanguageCreate', 'LanguageUpdate',
    'PublisherResponse', 'PublisherShortResponse', 'PublisherCreate',
    'PublisherUpdate'
]

