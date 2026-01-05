"""
Pydantic models for Meditation feature
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MeditationSession(BaseModel):
    """Meditation session metadata"""
    id: str
    tab: int  # 1 or 2
    title: str
    description: str
    audio_file: str
    duration_seconds: int
    category: str  # "introduction" or "beginner_course"
    order: int  # Display order


class MeditationProgress(BaseModel):
    """User's meditation progress"""
    user_id: str
    session_id: str
    completed: bool = False
    completed_at: Optional[datetime] = None
    time_spent: int = 0  # seconds
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MeditationStats(BaseModel):
    """User's meditation statistics"""
    total_sessions_completed: int
    total_time_spent: int  # seconds
    current_streak: int
    longest_streak: int
    introduction_completed: int  # out of 4
    beginner_course_completed: int  # out of 10
    last_session_date: Optional[datetime] = None
