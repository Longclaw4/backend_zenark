"""
Business logic for Meditation feature
"""

import logging
from datetime import datetime, timedelta, date as date_type
from typing import Optional, List, Dict, Any
from .database import get_meditation_progress_collection, get_meditation_streaks_collection
from .data import get_all_sessions, get_session_by_id, get_sessions_by_tab
from .models import MeditationStats

logger = logging.getLogger("zenark.meditation.service")


async def mark_session_complete(
    user_id: str,
    session_id: str,
    time_spent: int
) -> Dict[str, Any]:
    """
    Mark a meditation session as complete
    
    Args:
        user_id: User identifier
        session_id: Session ID (101-104, 201-210)
        time_spent: Time spent in seconds
    
    Returns:
        Dict with success status and streak info
    """
    try:
        progress_col = get_meditation_progress_collection()
        
        # Check if session exists
        session = get_session_by_id(session_id)
        if not session:
            return {"success": False, "error": "Invalid session ID"}
        
        # Update or create progress
        progress_data = {
            "user_id": user_id,
            "session_id": session_id,
            "completed": True,
            "completed_at": datetime.utcnow(),
            "time_spent": time_spent,
            "updated_at": datetime.utcnow()
        }
        
        await progress_col.update_one(
            {"user_id": user_id, "session_id": session_id},
            {"$set": progress_data, "$setOnInsert": {"created_at": datetime.utcnow()}},
            upsert=True
        )
        
        # Update streak if time spent >= 2 minutes
        streak_updated = False
        current_streak = 0
        
        if time_spent >= 120:  # 2 minutes
            streak_updated = await update_meditation_streak(user_id, time_spent)
            current_streak = await get_current_streak(user_id)
        
        logger.info(f"✅ Session {session_id} completed for user {user_id}")
        
        return {
            "success": True,
            "message": "Session completed successfully",
            "streak_updated": streak_updated,
            "current_streak": current_streak
        }
        
    except Exception as e:
        logger.error(f"Error marking session complete: {e}")
        return {"success": False, "error": str(e)}


async def update_meditation_streak(user_id: str, time_spent: int) -> bool:
    """
    Update user's meditation streak
    
    Args:
        user_id: User identifier
        time_spent: Time spent in seconds
    
    Returns:
        True if streak was updated
    """
    if time_spent < 120:  # Less than 2 minutes
        return False
    
    streaks_col = get_meditation_streaks_collection()
    
    streak_data = await streaks_col.find_one({"user_id": user_id})
    
    today = datetime.combine(datetime.utcnow().date(), datetime.min.time())
    
    if not streak_data:
        # Create new streak
        await streaks_col.insert_one({
            "user_id": user_id,
            "current_streak": 1,
            "longest_streak": 1,
            "last_meditation_date": today,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        return True
    
    # Convert last_meditation_date to date for comparison
    last_date = streak_data["last_meditation_date"]
    if isinstance(last_date, datetime):
        last_date = last_date.date()
    elif isinstance(last_date, date_type):
        pass
    else:
        last_date = datetime.utcnow().date()
    
    today_date = datetime.utcnow().date()
    
    # Check if already meditated today
    if last_date == today_date:
        return False
    
    # Check if yesterday
    yesterday = today_date - timedelta(days=1)
    
    if last_date == yesterday:
        # Continue streak
        new_streak = streak_data["current_streak"] + 1
        longest = max(new_streak, streak_data.get("longest_streak", 0))
        
        await streaks_col.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "current_streak": new_streak,
                    "longest_streak": longest,
                    "last_meditation_date": today,
                    "updated_at": datetime.utcnow()
                }
            }
        )
    else:
        # Streak broken, restart
        await streaks_col.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "current_streak": 1,
                    "last_meditation_date": today,
                    "updated_at": datetime.utcnow()
                }
            }
        )
    
    return True


async def get_current_streak(user_id: str) -> int:
    """Get user's current meditation streak"""
    streaks_col = get_meditation_streaks_collection()
    streak_data = await streaks_col.find_one({"user_id": user_id})
    
    if not streak_data:
        return 0
    
    # Check if streak is still valid (meditated yesterday or today)
    last_date = streak_data["last_meditation_date"]
    if isinstance(last_date, datetime):
        last_date = last_date.date()
    
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    
    if last_date in [today, yesterday]:
        return streak_data.get("current_streak", 0)
    else:
        # Streak expired
        return 0


async def get_user_progress(user_id: str) -> List[Dict[str, Any]]:
    """Get all completed sessions for a user"""
    progress_col = get_meditation_progress_collection()
    
    progress = await progress_col.find({
        "user_id": user_id,
        "completed": True
    }).to_list(length=None)
    
    result = []
    for p in progress:
        session = get_session_by_id(p["session_id"])
        if session:
            result.append({
                "session_id": p["session_id"],
                "title": session["title"],
                "completed_at": p["completed_at"].isoformat() if p.get("completed_at") else None,
                "time_spent": p.get("time_spent", 0)
            })
    
    return result


async def get_meditation_stats(user_id: str) -> MeditationStats:
    """Get comprehensive meditation statistics for a user"""
    progress_col = get_meditation_progress_collection()
    streaks_col = get_meditation_streaks_collection()
    
    # Get all completed sessions
    completed = await progress_col.find({
        "user_id": user_id,
        "completed": True
    }).to_list(length=None)
    
    # Calculate stats
    total_sessions = len(completed)
    total_time = sum(p.get("time_spent", 0) for p in completed)
    
    # Count by category
    intro_count = sum(1 for p in completed if p["session_id"].startswith("1"))
    beginner_count = sum(1 for p in completed if p["session_id"].startswith("2"))
    
    # Get streak data
    streak_data = await streaks_col.find_one({"user_id": user_id})
    current_streak = await get_current_streak(user_id)
    longest_streak = streak_data.get("longest_streak", 0) if streak_data else 0
    
    # Get last session date
    last_session = None
    if completed:
        last_session = max(p.get("completed_at") for p in completed if p.get("completed_at"))
    
    return MeditationStats(
        total_sessions_completed=total_sessions,
        total_time_spent=total_time,
        current_streak=current_streak,
        longest_streak=longest_streak,
        introduction_completed=intro_count,
        beginner_course_completed=beginner_count,
        last_session_date=last_session
    )
