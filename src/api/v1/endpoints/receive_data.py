from fastapi import APIRouter, Depends
from src.schemas.data_inp import ArduinoData, ArduinoResponse
from src.api.v1.dependencies.recieve_data import get_current_device

router = APIRouter()

@router.post("/", response_model=ArduinoResponse)
async def receive_data(
    data: ArduinoData,
    device: dict = Depends(get_current_device)  # ← проверка устройства!
):
    """
    Принимает данные от Arduino. Требует API-ключ в заголовке X-API-Key
    """
    # Теперь device содержит информацию об устройстве
    device_id = device['device_id']
    user_id = device['user_id']
    
    print(data)
    print(device_id, user_id)

    return ArduinoResponse()