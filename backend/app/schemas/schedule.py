# app/schemas/schedule.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScheduleBase(BaseModel):
    routine_id: int
    interval_seconds: int
    is_active: bool = True

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    interval_seconds: Optional[int] = None
    is_active: Optional[bool] = None

class ScheduleResponse(ScheduleBase):
    id: int
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ScheduleInDB(ScheduleResponse):
    pass