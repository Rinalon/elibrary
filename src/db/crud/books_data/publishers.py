from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.db.models import Publisher, Book, BookChangeable
from src.db.schemas import PublisherCreate, PublisherUpdate
from src.db.crud.base import BaseCRUD
from typing import Any, Optional, Tuple


class PublisherCRUD(BaseCRUD[Publisher, PublisherCreate, PublisherUpdate]):
    async def get_by_id(
            self,
            db: AsyncSession,
            item_id: int,
            load_options: Optional[Tuple[Any]] = None
    ) -> Publisher | None:
        if load_options is None:
            load_options = (
                selectinload(Publisher.books).joinedload(Book.changeable).load_only(BookChangeable.rating),
            )

        return await super().get_by_id(db, item_id, load_options)

