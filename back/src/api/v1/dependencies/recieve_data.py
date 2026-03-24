from src.services.device_auth import verify_device
from src.core.database import db
from fastapi import HTTPException, Header
from datetime import datetime

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

import json
from typing import Any
from datetime import datetime

async def save_readings_batch(device_id: int, readings: dict, received_at: datetime):
    """
    Сохраняет показания датчиков, автоматически определяя тип данных.
    
    - Числа → sensor_metrics_numeric
    - Boolean → sensor_metrics_boolean  
    - Строки и JSON → sensor_metrics_text
    """
    if not readings:
        return
    
    # Разделяем по типам
    numeric_params = []
    boolean_params = []
    text_params = []
    
    for metric_name, value in readings.items():
        if value is None:
            continue
        
        # Определяем тип и добавляем в соответствующий список
        if isinstance(value, bool):
            boolean_params.append((device_id, metric_name, value, received_at))
            
        elif isinstance(value, (int, float)):
            # Преобразуем в float для единообразия
            numeric_params.append((device_id, metric_name, float(value), received_at))
            
        elif isinstance(value, (dict, list)):
            # JSON данные сохраняем как строку
            text_params.append((device_id, metric_name, json.dumps(value, ensure_ascii=False), received_at))
            
        elif isinstance(value, str):
            text_params.append((device_id, metric_name, value, received_at))
            
        else:
            # Любые другие типы → в текст
            text_params.append((device_id, metric_name, str(value), received_at))
    
    # Массовая вставка числовых показаний
    if numeric_params:
        await db.executemany(
            """
            INSERT INTO sensor_metrics_numeric (device_id, metric_name, value, received_at)
            VALUES (%s, %s, %s, %s)
            """,
            numeric_params
        )
    
    # Массовая вставка булевых показаний
    if boolean_params:
        await db.executemany(
            """
            INSERT INTO sensor_metrics_boolean (device_id, metric_name, value, received_at)
            VALUES (%s, %s, %s, %s)
            """,
            boolean_params
        )
    
    # Массовая вставка текстовых показаний
    if text_params:
        await db.executemany(
            """
            INSERT INTO sensor_metrics_text (device_id, metric_name, value, received_at)
            VALUES (%s, %s, %s, %s)
            """,
            text_params
        )
    
    # Логируем результат
    total = len(numeric_params) + len(boolean_params) + len(text_params)
    if total > 0:
        print(f"💾 Saved {total} readings for device {device_id} "
               f"(numeric: {len(numeric_params)}, "
               f"boolean: {len(boolean_params)}, "
               f"text: {len(text_params)})")