# app/models/schedule.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from app.db.base_class import Base
from datetime import datetime

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(Integer, ForeignKey("routines.id"))
    interval_seconds = Column(Integer)  # Simple interval in seconds
    is_active = Column(Boolean, default=True)
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# TO-DO: Implement database models and functions for schedules
