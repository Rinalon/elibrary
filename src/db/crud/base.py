from sqlalchemy import select, update as sql_update
from typing import (
    Any,
    TypeVar,
    Generic,
    List,
    Tuple,
    Optional
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.exc import IntegrityError
from src.core.exceptions import NotFoundError, ConflictError

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType):
        self.model = model

    def _integrity_error_parser(self, error: IntegrityError):
        msg = str(error.orig)
        if "duplicate key" in msg:
            raise ConflictError(f"{self.model.__name__} already exists")
        if "foreign key" in msg:
            raise ConflictError("Referenced resource does not exist")
        raise

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
    ) -> ModelType | None:
        """Универсальная функция для получения записи по ID с опциональной подгрузкой."""
        pk = self.model.__table__.primary_key.columns.values()[0]

        query = select(self.model).where(pk == item_id)
        if load_options is not None:
            for option in load_options:
                query = query.options(option)

        result = await db.execute(query)

        if load_options:
            result = result.unique().scalar_one_or_none()
        else:
            result = result.scalar_one_or_none()

        if result is None:
            raise NotFoundError(f"{self.model.__name__} not found")

        return result

    async def create(
            self,
            db: AsyncSession,
            data: CreateSchemaType
    ) -> ModelType:
        """Универсальная функция создания"""
        new_item = self.model(data.model_dump())

        db.add(new_item)
        try:
            await db.commit()
            await db.refresh(new_item)
            return new_item
        except IntegrityError as e:
            self._integrity_error_parser(e)

    async def update(
            self,
            db: AsyncSession,
            item_id: int,
            data: UpdateSchemaType,
            load_options: Optional[Tuple[Any]] = None,
    ) -> ModelType | None:
        """Универсальная функция обновления"""
        pk = self.model.__table__.primary_key.columns.values()[0]

        result = await db.execute(
            sql_update(self.model)
            .where(pk == item_id)
            .values(data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        await db.commit()
        try:
            item = result.scalar_one_or_none()
            if item and load_options:
                return await self.get_by_id(db, item_id, load_options=load_options)

            return item
        except IntegrityError as e:
            self._integrity_error_parser(e)