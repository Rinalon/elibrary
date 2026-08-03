from sqlalchemy import select
from typing import (
    Type,
    Any,
    TypeVar,
    Generic,
    List,
    Tuple,
    Optional
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import ClauseElement

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")

class BaseCRUD(Generic[ModelType, CreateSchemaType]):
    default_load_options_for_get = ()
    default_load_options_for_list = ()

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(self, db: AsyncSession) -> List[ModelType]:
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def get_paginate(
            self,
            db: AsyncSession,
            limit: int = 10,
            offset: int = 0,
            order: Optional[Tuple[ClauseElement]] = None,
            load_options: Optional[Tuple[Any]] = None,
    ) -> List[ModelType]:
        pk = self.model.__table__.primary_key.columns.values()[0]

        query = select(self.model).limit(limit).offset(offset)

        if order is None:
            order = (pk,)

        for condition in order:
            query = query.order_by(condition)

        if load_options is not None:
            for option in load_options:
                query = query.options(option)

        result = await db.execute(query)
        return result.scalars().all()


    async def get_by_id(
            self,
            db: AsyncSession,
            item_id: int,
            load_options: Optional[Tuple[Any]] = None
    ) -> Any | None:
        """Универсальная функция для получения записи по ID с опциональной подгрузкой."""
        pk = self.model.__table__.primary_key.columns.values()[0]

        query = select(self.model).where(pk == item_id)
        if load_options is not None:
            for option in load_options:
                query = query.options(option)

        result = await db.execute(query)

        if load_options:
            return result.unique().scalar_one_or_none()
        return result.scalar_one_or_none()

    async def create(
            self,
            db: AsyncSession,
            data: CreateSchemaType
    ):
        """Универсальная функция создания"""
        new_item = self.model(data.model_dump())

        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)

        return new_item
