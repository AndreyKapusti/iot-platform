from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class DeviceResponse(BaseModel):
    id: int
    name: str
    api_key: str
    is_active: bool
    created_at: datetime

class DeviceAuth(BaseModel):
    device_id: str
    api_key: str