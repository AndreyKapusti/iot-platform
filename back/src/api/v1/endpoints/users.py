from fastapi import APIRouter, Depends, HTTPException
from src.core.database import db
from src.schemas.user import UserResponse
from src.api.v1.dependencies.users import get_current_user

router = APIRouter()

@router.get('/me', response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    return current_user