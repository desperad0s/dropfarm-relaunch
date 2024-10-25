# app/api/v1/routines.py
from fastapi import APIRouter, Depends
from app.services.automation.automation_service import AutomationService
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/routines/start-recording")
async def start_recording(user = Depends(get_current_user)):
    # Create user-specific automation service
    user_data_dir = f"browser_data/{user.id}"
    automation = AutomationService(user_data_dir)
    await automation.start_browser()
    await automation.start_recording()
    return {"status": "recording_started"}

@router.post("/routines/stop-recording")
async def stop_recording(user = Depends(get_current_user)):
    # Get user's automation service
    automation = AutomationService(f"browser_data/{user.id}")
    recorded_steps = await automation.stop_recording()
    await automation.close()
    return {"recorded_steps": recorded_steps}

@router.post("/routines/{routine_id}/play")
async def play_routine(routine_id: int, user = Depends(get_current_user)):
    # Get routine from database
    routine = await get_routine(routine_id)  # TO-DO: Implement this
    # Play back the routine
    automation = AutomationService(f"browser_data/{user.id}")
    await automation.start_browser()
    await automation.playback_routine(routine.steps)
    await automation.close()
    return {"status": "playback_completed"}

# TO-DO: Implement routines endpoints