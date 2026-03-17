from fastapi import FastAPI
from src.core.config import settings
from src.api.v1.api import api_router
from contextlib import asynccontextmanager
from src.core.database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "IoT Platform API"}

@app.get("/health")
async def health():
    return {"status": "ok"}