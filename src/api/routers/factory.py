from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, List, Any, Optional
from src.core.database import get_db

def create_crud_router(
        prefix: str,
        tag: str,
        crud_class: Any,
        response_schema: Type,
        create_schema: Type,
        short_response_schema: Optional[Type] = None,
        update_schema: Optional[Type] = None,
        paginated: bool = True,
):
    """
    Фабрика для создания CRUD-роутеров.

    :param prefix: Префикс URL (например, "/books")
    :param tag: Тег для Swagger (например, "books")
    :param crud_class: Класс CRUD (BookCRUD, AuthorCRUD, ...)
    :param response_schema: Полная схема ответа (BookResponse, ...)
    :param short_response_schema: Краткая схема для списка (BookShortResponse, ...)
    :param create_schema: Схема для создания (BookCreate, ...)
    :param update_schema: Схема для обновления (BookUpdate, ...)
    :param paginated: Использовать пагинацию (True/False)
    """

    router = APIRouter(prefix=prefix, tags=[tag])
    crud_instance = crud_class

    # 1. GET /
    if paginated:
        @router.get("/", response_model=List[short_response_schema], response_model_exclude_none=True)
        async def get_all(
                page: int = 1,
                size: int = 10,
                db: AsyncSession = Depends(get_db)
        ):
            items = await crud_instance.get_paginate(
                db=db,
                limit=size,
                offset=(page - 1) * size
            )
            return items if items else []
    else:
        @router.get("/", response_model=List[short_response_schema], response_model_exclude_none=True)
        async def get_all(
                db: AsyncSession = Depends(get_db)
        ):
            items = await crud_instance.get_all(db=db)
            return items if items else []

    # 2. GET /{id}
    if short_response_schema:
        @router.get("/{item_id}", response_model=response_schema, response_model_exclude_none=True)
        async def get_one(
                item_id: int,
                db: AsyncSession = Depends(get_db)
        ):
            item = await crud_instance.get_by_id(db, item_id)
            if not item:
                raise HTTPException(404, f"{tag.capitalize()[:-1]} not found")
            return item

    # 3. POST /
    @router.post("/", response_model=response_schema)
    async def create_one(
            data: create_schema,
            db: AsyncSession = Depends(get_db)
    ):
        try:
            new_item = await crud_instance.create(db, data)
            return new_item
        except Exception as e:
            raise HTTPException(500, str(e))

    # 4. PATCH /{id}
    @router.patch("/{id}", response_model=response_schema, response_model_exclude_none=True)
    async def update_one(
            id: int,
            data: update_schema,
            db: AsyncSession = Depends(get_db)
    ):
        try:
            updated_item = await crud_instance.update(db, id, data)
            return updated_item
        except Exception as e:
            raise HTTPException(500, str(e))

    return router