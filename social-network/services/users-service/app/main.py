from fastapi import FastAPI
from .database import Base, engine
from .routes import router

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Users Service API")

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}