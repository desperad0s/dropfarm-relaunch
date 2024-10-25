# backend/app/main.py
"""
Main FastAPI application entry point
filepath: backend/app/main.py
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, routines, schedules

app = FastAPI(title="Dropfarm API")

# TODO: Configure CORS properly for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(routines.router, prefix="/api/v1")
app.include_router(schedules.router, prefix="/api/v1")

# TO-DO: Implement main application logic
