from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.data_inp import Datamodel_inp
from src.api.v1.dependencies.recieve_data import get_current_device, save_readings_batch
from datetime import datetime, timezone

router = APIRouter()

@router.post("/")
async def receive_data(
    data: Datamodel_inp,
    device: dict = Depends(get_current_device)  # ← проверка устройства!
):
    """
    Принимает данные от Arduino. Требует API-ключ в заголовке X-API-Key
    """
    # Теперь device содержит информацию об устройстве
    device_id = device['id']
    user_id = device['user_id']

    if device_id != data.device_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный id устройства в JSON'
        )
    
    data_to_load = data.readings
    await save_readings_batch(device_id, data_to_load, datetime.now(timezone.utc))