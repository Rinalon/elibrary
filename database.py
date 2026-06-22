from config import settings
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_engine(
    url=settings.database_url_psycopg,
    echo=False,
    #pool_size=5,
    #max_overflow=2
)

'''
async_engine = create_async_engine(
    url=settings.database_url_async,
    echo=False,
    #pool_size=5,
    #max_overflow=2
)
'''

with engine.connect() as conn:

   conn.commit()

'''
async def get_a():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT * FROM books WHERE book_id < 5 ORDER BY book_id"))
        print(f"{res.all()}")
'''