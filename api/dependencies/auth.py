from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
#from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from crud.users_base import  get_user_by_id
from core.database import get_db
#from core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(404, "User not found")
    return user