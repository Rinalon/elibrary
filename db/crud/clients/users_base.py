from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User

async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(
        select(User).where(User.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def get_user_by_login(db: AsyncSession, login: str) -> User | None:
    result = await db.execute(
        select(User).where(User.login == login)
    )
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_data: dict) -> User:
    db_user = User(**user_data)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user