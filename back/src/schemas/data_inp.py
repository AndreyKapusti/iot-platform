from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime

class ArduinoData(BaseModel):
    temperature: Optional[float] = Field(
        None,
        description="Температура в градусах Цельсия",
        ge=-50,  # больше или равно -50
        le=150,   # меньше или равно 150
        examples=[23.5, 25.1, 18.7]
    )
    
    humidity: Optional[float] = Field(
        None,
        description="Влажность в процентах",
        ge=0,
        le=100,
        examples=[45, 60, 72.5]
    )
    
    light: Optional[float] = Field(
        None,
        description="Освещенность в люксах",
        ge=0,
        le=100000,
        examples=[150, 450, 800]
    )
    
    pressure: Optional[float] = Field(
        None,
        description="Атмосферное давление в гПа",
        ge=800,
        le=1200,
        examples=[1013.25, 1008.5]
    )
    
    co2: Optional[int] = Field(
        None,
        description="Уровень CO2 в ppm",
        ge=0,
        le=5000,
        examples=[400, 450, 1200]
    )
    
    motion: Optional[bool] = Field(
        None,
        description="Детектор движения (true/false)",
        examples=[True, False]
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Дополнительные данные в свободном формате"
    )

    @field_validator('temperature')
    def validate_temperature(cls, v):
        """Кастомная валидация температуры"""
        if v is not None and v < -50:
            raise ValueError('Температура не может быть ниже -50°C')
        return v
    
    class Config:
        """Настройки для документации Swagger"""
        json_schema_extra = {
            "example": {
                "temperature": 23.5,
                "humidity": 60,
                "light": 450,
                "pressure": 1013.25,
                "co2": 420,
                "motion": False,
                "metadata": {
                    "firmware": "2.1.0",
                    "battery": 85
                }
            },
        }

class ArduinoResponse(BaseModel):
    """
    Ответ сервера Arduino - состояния актуаторов
    """
    led: bool = Field(False, description="Состояние светодиода")
    fan: bool = Field(False, description="Состояние вентилятора")
    servo: bool = Field(False, description="Состояние сервопривода")
    pomp: bool = Field(False, description="Состояние помпы")
    
    server_timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Время ответа сервера"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "led": True,
                "fan": False,
                "servo": True,
                "pomp": False,
                "server_timestamp": "2024-03-19T15:30:05Z"
            }
        }