from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
#from core.security import hash_password, verify_password, create_access_token
#from crud.user_crud import get_user_by_login, create_user
#from schemas.user import UserCreate

"""
async def register_user(db: AsyncSession, user_data: UserCreate):
    # 1. Проверяем, существует ли пользователь
    existing_user = await get_user_by_login(db, user_data.login)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")

    # 2. Создаём объект для БД (хешируем пароль)
    new_user_data = user_data.model_dump(exclude={"password"})
    new_user_data["password_hash"] = hash_password(user_data.password)

    # 3. Сохраняем в БД
    db_user = await create_user(db, new_user_data)

    # 4. Генерируем токен
    token = create_access_token({"sub": str(db_user.user_id)})

    return {"user": db_user, "access_token": token}
"""