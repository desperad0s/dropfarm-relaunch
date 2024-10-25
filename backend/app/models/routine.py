# app/models/routine.py
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from app.db.base_class import Base
from datetime import datetime

class Routine(Base):
    __tablename__ = "routines"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    description = Column(String, nullable=True)
    steps = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# TO-DO: Implement database models and functions for routines
