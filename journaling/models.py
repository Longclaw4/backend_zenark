"""
Data Models for Journaling Feature
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class JournalEntry(BaseModel):
    """Journal entry model"""
    user_id: str
    mood: str  # Emoji: 😊 😃 😐 😢
    title: str
    content: str
    tags: List[str] = []
    time_spent: int = 0  # Time spent in seconds
    is_favorite: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            ObjectId: lambda v: str(v)
        }


class JournalEntryCreate(BaseModel):
    """Request model for creating a journal entry"""
    user_id: str
    mood: str
    title: str
    content: str
    tags: List[str] = []
    time_spent: int = 0


class JournalEntryUpdate(BaseModel):
    """Request model for updating a journal entry"""
    mood: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class JournalStreak(BaseModel):
    """User's journaling streak data"""
    user_id: str
    current_streak: int = 0
    last_entry_date: Optional[datetime] = None
    longest_streak: int = 0
    total_days: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DailyPrompt(BaseModel):
    """Daily journaling prompt"""
    prompt_id: str
    text: str
    category: str  # reflection, gratitude, goals, emotions
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class JournalStats(BaseModel):
    """User's journaling statistics"""
    total_entries: int
    current_streak: int
    longest_streak: int
    total_days: int
    mood_distribution: dict
    most_used_tags: List[dict]
    total_time_spent: int  # Total seconds spent journaling
    average_time_per_entry: int
