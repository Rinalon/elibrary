import uvicorn
from fastapi import FastAPI
from api.routers import (
    books_router,
    author_router,
    genre_router
)

app = FastAPI(title="E-Library API", version="1.0.0")

app.include_router(books_router)
app.include_router(author_router)
app.include_router(genre_router)
@app.get("/")
async def root():
    return {"message": "E-Library API is running"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )