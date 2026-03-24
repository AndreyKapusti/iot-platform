from fastapi import HTTPException
from src.core.database import db
import secrets

async def verify_device(api_key: str):
    """
    Проверяет API ключ и возвращает данные устройства
    """
    device = await db.fetch_one(
        """
        SELECT id, user_id, name, is_active
        FROM devices
        WHERE api_key = %s AND is_active = true
        """,
        api_key
    )

    if not device:
        return None
    
    return dict(device)

async def generate_api_key() -> str:
    return secrets.token_urlsafe(32)

async def create_device(user_id: int, name: str):
    """
    Создаёт новое устройство с уникальным API ключом,
    добавляет его в таблицу устройств
    """
    api_key = await generate_api_key()

    try:
        row = await db.fetch_one(
            """
            INSERT INTO devices (name, api_key, user_id)
            VALUES (%s, %s, %s)
            RETURNING id, name, api_key, is_active, created_at
            """,
            name, api_key, user_id
        )

    except Exception as e:
        if 'duplicate key' in str(e).lower():
            raise HTTPException(
                status_code=400,
                detail=f"You already have a device with name '{name}'"
            )
        raise

    return dict(row)