from src.services.device_auth import verify_device
from fastapi import APIRouter, HTTPException, Header

async def get_current_device(x_api_key: str = Header(...)):
    """
    Проверяет API-ключ устройства и возвращает device_id
    """
    device = await verify_device(x_api_key)
    if not device:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return device