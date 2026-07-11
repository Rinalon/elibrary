from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreate
from services.auth_service import register_user
from core.database import get_db

router = APIRouter(prefix="/register", tags=["register"])

@router.post("/register")
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await register_user(db, user_data)