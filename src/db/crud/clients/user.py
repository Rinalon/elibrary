from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User
from src.db.schemas import UserCreate
from src.db.crud.base import BaseCRUD

class UserCRUD(BaseCRUD[User, UserCreate]):
    async def get_by_login(self, db: AsyncSession, login: str) -> User | None:
        result = await db.execute(
            select(User).where(User.login == login)
        )
        return result.scalar_one_or_none()
