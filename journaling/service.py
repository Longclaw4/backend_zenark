"""
Business logic for Journaling feature
Handles streak calculation, entry management, and statistics
"""

from datetime import datetime, timedelta, date
from typing import List, Dict, Optional
from bson import ObjectId
import logging
import random

from .database import (
    get_journal_entries_collection,
    get_journal_streaks_collection,
    get_daily_prompts_collection
)
from .models import JournalEntry, JournalStreak, JournalStats

logger = logging.getLogger("zenark.journaling.service")


async def create_journal_entry(
    user_id: str,
    mood: str,
    title: str,
    content: str,
    tags: List[str],
    time_spent: int
) -> Dict:
    """
    Create a new journal entry
    
    Args:
        user_id: User identifier
        mood: Mood emoji
        title: Entry title
        content: Entry content
        tags: List of tags
        time_spent: Time spent in seconds
    
    Returns:
        Dict with entry_id, streak info
    """
    entries_col = get_journal_entries_collection()
    
    # Create entry document
    entry = {
        "user_id": user_id,
        "mood": mood,
        "title": title,
        "content": content,
        "tags": tags,
        "time_spent": time_spent,
        "is_favorite": False,
        "timestamp": datetime.utcnow(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Save to database
    result = await entries_col.insert_one(entry)
    entry_id = str(result.inserted_id)
    
    # Update streak if time spent >= 5 minutes (300 seconds)
    streak_updated = False
    current_streak = 0
    
    if time_spent >= 300:
        streak_updated = await update_user_streak(user_id, time_spent)
        current_streak = await get_user_current_streak(user_id)
    
    logger.info(f"✅ Created journal entry {entry_id} for user {user_id}")
    
    return {
        "entry_id": entry_id,
        "streak_updated": streak_updated,
        "current_streak": current_streak
    }


async def get_recent_entries(user_id: str, limit: int = 5) -> List[Dict]:
    """
    Get user's recent journal entries
    
    Args:
        user_id: User identifier
        limit: Number of entries to return
    
    Returns:
        List of recent entries with formatted dates
    """
    entries_col = get_journal_entries_collection()
    
    entries = await entries_col.find({
        "user_id": user_id
    }).sort("timestamp", -1).limit(limit).to_list(length=limit)
    
    # Format entries
    formatted_entries = []
    for entry in entries:
        formatted_entries.append({
            "id": str(entry["_id"]),
            "date": format_date(entry["timestamp"]),
            "timestamp": entry["timestamp"].isoformat(),
            "title": entry["title"],
            "preview": create_preview(entry["content"]),
            "mood": entry["mood"],
            "tags": entry.get("tags", []),
            "time_spent": entry.get("time_spent", 0),
            "is_favorite": entry.get("is_favorite", False)
        })
    
    return formatted_entries


async def get_entry_by_id(entry_id: str, user_id: str) -> Optional[Dict]:
    """Get a specific journal entry by ID"""
    entries_col = get_journal_entries_collection()
    
    entry = await entries_col.find_one({
        "_id": ObjectId(entry_id),
        "user_id": user_id
    })
    
    if not entry:
        return None
    
    return {
        "id": str(entry["_id"]),
        "user_id": entry["user_id"],
        "mood": entry["mood"],
        "title": entry["title"],
        "content": entry["content"],
        "tags": entry.get("tags", []),
        "time_spent": entry.get("time_spent", 0),
        "is_favorite": entry.get("is_favorite", False),
        "timestamp": entry["timestamp"].isoformat(),
        "created_at": entry["created_at"].isoformat(),
        "updated_at": entry["updated_at"].isoformat()
    }


async def update_journal_entry(
    entry_id: str,
    user_id: str,
    mood: Optional[str] = None,
    title: Optional[str] = None,
    content: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> bool:
    """Update an existing journal entry"""
    entries_col = get_journal_entries_collection()
    
    update_data = {"updated_at": datetime.utcnow()}
    
    if mood is not None:
        update_data["mood"] = mood
    if title is not None:
        update_data["title"] = title
    if content is not None:
        update_data["content"] = content
    if tags is not None:
        update_data["tags"] = tags
    
    result = await entries_col.update_one(
        {"_id": ObjectId(entry_id), "user_id": user_id},
        {"$set": update_data}
    )
    
    return result.modified_count > 0


async def delete_journal_entry(entry_id: str, user_id: str) -> bool:
    """Delete a journal entry"""
    entries_col = get_journal_entries_collection()
    
    result = await entries_col.delete_one({
        "_id": ObjectId(entry_id),
        "user_id": user_id
    })
    
    return result.deleted_count > 0


async def toggle_favorite(entry_id: str, user_id: str) -> Dict:
    """Toggle favorite status of an entry"""
    entries_col = get_journal_entries_collection()
    
    entry = await entries_col.find_one({
        "_id": ObjectId(entry_id),
        "user_id": user_id
    })
    
    if not entry:
        return {"success": False, "error": "Entry not found"}
    
    new_status = not entry.get("is_favorite", False)
    
    await entries_col.update_one(
        {"_id": ObjectId(entry_id)},
        {
            "$set": {
                "is_favorite": new_status,
                "favorited_at": datetime.utcnow() if new_status else None,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {
        "success": True,
        "is_favorite": new_status,
        "message": "Added to favorites" if new_status else "Removed from favorites"
    }


async def get_favorites(user_id: str) -> List[Dict]:
    """Get all favorite entries for a user"""
    entries_col = get_journal_entries_collection()
    
    favorites = await entries_col.find({
        "user_id": user_id,
        "is_favorite": True
    }).sort("favorited_at", -1).to_list(length=None)
    
    formatted_favorites = []
    for entry in favorites:
        formatted_favorites.append({
            "id": str(entry["_id"]),
            "date": format_date(entry["timestamp"]),
            "timestamp": entry["timestamp"].isoformat(),
            "title": entry["title"],
            "preview": create_preview(entry["content"]),
            "mood": entry["mood"],
            "tags": entry.get("tags", []),
            "favorited_at": entry.get("favorited_at", entry["timestamp"]).isoformat()
        })
    
    return formatted_favorites


async def get_past_reflections(user_id: str, target_date: Optional[date] = None) -> Dict:
    """
    Get journal entries for a specific date
    
    Args:
        user_id: User identifier
        target_date: Date to get entries for (defaults to today)
    
    Returns:
        Dict with entries for that date
    """
    entries_col = get_journal_entries_collection()
    
    if target_date is None:
        target_date = datetime.utcnow().date()
    
    # Get start and end of day
    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = datetime.combine(target_date, datetime.max.time())
    
    entries = await entries_col.find({
        "user_id": user_id,
        "timestamp": {"$gte": start_of_day, "$lte": end_of_day}
    }).sort("timestamp", -1).to_list(length=None)
    
    formatted_entries = []
    total_time = 0
    
    for entry in entries:
        formatted_entries.append({
            "id": str(entry["_id"]),
            "time": entry["timestamp"].strftime("%I:%M %p"),
            "title": entry["title"],
            "preview": create_preview(entry["content"]),
            "mood": entry["mood"],
            "tags": entry.get("tags", []),
            "time_spent": entry.get("time_spent", 0),
            "is_favorite": entry.get("is_favorite", False)
        })
        total_time += entry.get("time_spent", 0)
    
    return {
        "date": target_date.isoformat(),
        "entries": formatted_entries,
        "total_entries": len(formatted_entries),
        "total_time_spent": total_time
    }


async def get_calendar_data(user_id: str, year: int, month: int) -> Dict:
    """
    Get calendar data showing which dates have entries
    
    Args:
        user_id: User identifier
        year: Year
        month: Month (1-12)
    
    Returns:
        Dict with dates that have entries
    """
    entries_col = get_journal_entries_collection()
    
    # Get start and end of month
    month_start = datetime(year, month, 1)
    if month == 12:
        month_end = datetime(year + 1, 1, 1)
    else:
        month_end = datetime(year, month + 1, 1)
    
    # Aggregate entries by date
    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "timestamp": {"$gte": month_start, "$lt": month_end}
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}
                },
                "count": {"$sum": 1},
                "moods": {"$push": "$mood"}
            }
        },
        {
            "$sort": {"_id": 1}
        }
    ]
    
    results = await entries_col.aggregate(pipeline).to_list(length=None)
    
    dates_with_entries = []
    for result in results:
        # Get most common mood for the day
        moods = result["moods"]
        most_common_mood = max(set(moods), key=moods.count) if moods else "😐"
        
        dates_with_entries.append({
            "date": result["_id"],
            "count": result["count"],
            "mood": most_common_mood
        })
    
    return {
        "month": f"{year}-{month:02d}",
        "dates_with_entries": dates_with_entries
    }


async def update_user_streak(user_id: str, time_spent: int) -> bool:
    """
    Update user's journaling streak
    
    Args:
        user_id: User identifier
        time_spent: Time spent on entry in seconds
    
    Returns:
        True if streak was updated, False if already counted today
    """
    if time_spent < 300:  # Less than 5 minutes
        return False
    
    streaks_col = get_journal_streaks_collection()
    
    streak_data = await streaks_col.find_one({"user_id": user_id})
    
    today = datetime.utcnow().date()
    
    if not streak_data:
        # First time journaling
        await streaks_col.insert_one({
            "user_id": user_id,
            "current_streak": 1,
            "last_entry_date": datetime.combine(today, datetime.min.time()),  # Convert to datetime
            "longest_streak": 1,
            "total_days": 1,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        logger.info(f"✅ Started streak for user {user_id}")
        return True
    
    last_date = streak_data.get("last_entry_date")
    
    # Convert datetime to date if needed
    if isinstance(last_date, datetime):
        last_date = last_date.date()
    
    # Check if already journaled today
    if last_date == today:
        return False  # Already counted today
    
    # Check if consecutive day
    yesterday = today - timedelta(days=1)
    
    if last_date == yesterday:
        # Consecutive day - increment streak
        new_streak = streak_data["current_streak"] + 1
        logger.info(f"✅ Incremented streak for user {user_id}: {new_streak} days")
    else:
        # Missed days - reset streak
        new_streak = 1
        logger.info(f"⚠️ Reset streak for user {user_id} (missed days)")
    
    # Update longest streak if needed
    longest = max(new_streak, streak_data.get("longest_streak", 1))
    
    await streaks_col.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "current_streak": new_streak,
                "last_entry_date": datetime.combine(today, datetime.min.time()),  # Convert to datetime
                "longest_streak": longest,
                "total_days": streak_data.get("total_days", 0) + 1,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return True


async def get_user_current_streak(user_id: str) -> int:
    """Get user's current streak"""
    streaks_col = get_journal_streaks_collection()
    
    streak_data = await streaks_col.find_one({"user_id": user_id})
    
    if not streak_data:
        return 0
    
    # Check if streak is still valid (last entry was yesterday or today)
    last_date = streak_data.get("last_entry_date")
    
    # Convert datetime to date if needed
    if isinstance(last_date, datetime):
        last_date = last_date.date()
    
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    
    if last_date in [today, yesterday]:
        return streak_data.get("current_streak", 0)
    else:
        # Streak broken
        return 0


async def get_daily_prompt() -> Dict:
    """Get today's daily prompt (random)"""
    prompts_col = get_daily_prompts_collection()
    
    # Get all active prompts
    prompts = await prompts_col.find({"active": True}).to_list(length=None)
    
    if not prompts:
        return {
            "prompt_id": "default",
            "text": "How are you feeling today?",
            "category": "reflection"
        }
    
    # Select random prompt
    prompt = random.choice(prompts)
    
    return {
        "prompt_id": prompt["prompt_id"],
        "text": prompt["text"],
        "category": prompt["category"]
    }


async def get_user_stats(user_id: str) -> JournalStats:
    """Get comprehensive statistics for a user"""
    entries_col = get_journal_entries_collection()
    streaks_col = get_journal_streaks_collection()
    
    # Get total entries
    total_entries = await entries_col.count_documents({"user_id": user_id})
    
    # Get streak data
    streak_data = await streaks_col.find_one({"user_id": user_id})
    current_streak = await get_user_current_streak(user_id)
    longest_streak = streak_data.get("longest_streak", 0) if streak_data else 0
    total_days = streak_data.get("total_days", 0) if streak_data else 0
    
    # Get mood distribution
    mood_pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": "$mood", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    mood_results = await entries_col.aggregate(mood_pipeline).to_list(length=None)
    mood_distribution = {item["_id"]: item["count"] for item in mood_results}
    
    # Get most used tags
    tags_pipeline = [
        {"$match": {"user_id": user_id}},
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    tags_results = await entries_col.aggregate(tags_pipeline).to_list(length=10)
    most_used_tags = [{"tag": item["_id"], "count": item["count"]} for item in tags_results]
    
    # Get total time spent
    time_pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": None, "total_time": {"$sum": "$time_spent"}}}
    ]
    time_results = await entries_col.aggregate(time_pipeline).to_list(length=1)
    total_time_spent = time_results[0]["total_time"] if time_results else 0
    
    average_time = total_time_spent // total_entries if total_entries > 0 else 0
    
    return JournalStats(
        total_entries=total_entries,
        current_streak=current_streak,
        longest_streak=longest_streak,
        total_days=total_days,
        mood_distribution=mood_distribution,
        most_used_tags=most_used_tags,
        total_time_spent=total_time_spent,
        average_time_per_entry=average_time
    )


def format_date(timestamp: datetime) -> str:
    """Format date like 'Yesterday, 5:20 PM' or 'Sat Dec 21, 9:20 AM'"""
    now = datetime.utcnow()
    diff = (now.date() - timestamp.date()).days
    
    if diff == 0:
        return f"Today, {timestamp.strftime('%I:%M %p')}"
    elif diff == 1:
        return f"Yesterday, {timestamp.strftime('%I:%M %p')}"
    else:
        return timestamp.strftime("%a %b %d, %I:%M %p")


def create_preview(content: str, max_length: int = 150) -> str:
    """Create preview text from content"""
    if len(content) <= max_length:
        return content
    return content[:max_length].rsplit(' ', 1)[0] + "..."
