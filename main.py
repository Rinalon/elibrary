import uvicorn
from fastapi import FastAPI
from routers import books_router

app = FastAPI(title="E-Library API", version="1.0.0")

app.include_router(books_router)

@app.get("/")
async def root():
    return {"message": "E-Library API is running"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",      # путь к твоему приложению
        host="127.0.0.1", # локальный сервер
        port=8000,       # порт, на котором будет висеть API
        reload=True      # авто-перезагрузка при изменениях (удобно для разработки)
    )