from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class Datamodel_inp(BaseModel):
    """
    Универсальная модель для данных от любого устройства.
    Принимает любые поля в плоском JSON.
    """
    device_id: int = Field(
        ...,
        description="ID устройства будет сравниваться с ID из ключа, для предотвращения использования украденных ключей"
    )
    
    timestamp: Optional[datetime] = Field(
        None,
        description="Время на устройстве (если не указано, используется серверное)"
    )
    
    readings: Dict[str, Any] = Field(
        default_factory=dict,
        description="Показания датчиков в формате 'название_датчика': значение"
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Дополнительные метаданные (версия прошивки, заряд батареи и т.д.)"
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "device_id": 1,
                    "timestamp": "2024-03-24T15:30:00Z",
                    "readings": {
                        "temperature": 23.5,
                        "humidity": 60,
                        "light": 450,
                        "co2": 420,
                        "motion": False
                    },
                    "metadata": {
                        "firmware": "2.1.0",
                        "battery": 85,
                        "rssi": -67
                    }
                },
                {
                    "device_id": "vibration_sensor_01",
                    "readings": {
                        "vibration_x": 0.12,
                        "vibration_y": 0.08,
                        "vibration_z": 0.15,
                        "temperature": 45.2
                    }
                }
            ]
        }