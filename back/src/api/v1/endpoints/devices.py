from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.device import DeviceCreate, DeviceResponse
from src.services.device_auth import create_device, generate_api_key
from src.api.v1.dependencies.users import get_current_user
from src.core.database import db

router = APIRouter()

@router.post('/', response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def add_device(
    device_data: DeviceCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Добавление нового устройства.
    Только авторизованные пользователи могут добавлять устройства.
    """
    user_id = current_user['id']

    existing = await db.fetch_one(
        """
        SELECT device_id FROM devices
        WHERE device_id = %s AND user_id = %s
        """,
        device_data.device_id, user_id
    )

    if existing:
        print('ERR1')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You already have a device with ID '{device_data.device_id}'"
        )
    
    devices_count = await db.fetch_val(
        """
        SELECT COUNT(*) FROM devices WHERE user_id = %s
        """,
        user_id
    )
    
    if devices_count >= 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 10 devices per user"
        )
    
    device = await create_device(
        user_id=user_id,
        device_id=device_data.device_id,
        name=device_data.name
    )
    
    return device

@router.get("/")
async def get_user_devices(current_user: dict = Depends(get_current_user)):
    devices = await db.fetch_all(
        """
        SELECT device_id, name, api_key, is_active, created_at
        FROM devices
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        current_user['id']
    )
    return [dict(device) for device in devices]

@router.delete("/{device_id}")
async def delete_device(device_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user['id']
    
    # Проверяем, принадлежит ли устройство пользователю
    device = await db.fetch_one(
        """
        SELECT id FROM devices
        WHERE device_id = %s AND user_id = %s
        """,
        device_id, user_id
    )

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    await db.execute(
        "DELETE FROM devices WHERE device_id = %s AND user_id = %s",
        device_id, user_id
    )
    
    return {"status": "ok", "message": "Device deleted"}

@router.get("/{device_id}/api-key")
async def regenerate_api_key(device_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user['id']
    
    device = await db.fetch_one(
        """
        SELECT id FROM devices
        WHERE device_id = %s AND user_id = %s
        """,
        device_id, user_id
    )

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    new_api_key = await generate_api_key()
    
    await db.execute(
        """
        UPDATE devices SET api_key = %s
        WHERE device_id = %s AND user_id = %s
        """,
        new_api_key, device_id, user_id
    )
     
    return {"api_key": new_api_key}