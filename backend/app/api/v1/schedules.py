# backend/app/api/v1/schedules.py
"""
Schedule management endpoints
filepath: backend/app/api/v1/schedules.py
"""
from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.schemas.schedule import ScheduleCreate, ScheduleResponse

router = APIRouter()

@router.post("/schedules")
async def create_schedule(schedule: ScheduleCreate):
    """Create a new schedule."""
    # TODO: Implement schedule creation
    pass

@router.get("/schedules")
async def list_schedules():
    """List user's schedules."""
    # TODO: Implement schedules listing
    pass

# TO-DO: Implement schedules endpoints