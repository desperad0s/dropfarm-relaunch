# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core import security

router = APIRouter()

@router.post("/register")
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    # TODO: Implement user registration
    pass

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # TODO: Implement login
    pass

# TO-DO: Implement auth endpoints