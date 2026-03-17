from fastapi import APIRouter
from src.api.v1.endpoints import users, auth

api_router = APIRouter()

api_router.include_router(users.router, prefix="", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])