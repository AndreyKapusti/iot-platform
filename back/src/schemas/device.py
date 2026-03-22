from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceCreate(BaseModel):
    device_id: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)

class DeviceResponse(BaseModel):
    id: int
    device_id: str
    name: str
    api_key: str
    is_active: bool
    created_at: datetime

class DeviceAuth(BaseModel):
    device_id: str
    api_key: str