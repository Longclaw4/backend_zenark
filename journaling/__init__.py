"""
Journaling Module for Mental Health App
Provides journal entry management, mood tracking, and streak calculation
"""

from .routes import router
from .models import JournalEntry, JournalStreak, DailyPrompt
from .database import init_journaling_db

__all__ = ["router", "JournalEntry", "JournalStreak", "DailyPrompt", "init_journaling_db"]
