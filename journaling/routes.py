"""
FastAPI Routes for Journaling Feature
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime, date
from typing import Optional
import logging

from .models import JournalEntryCreate, JournalEntryUpdate
from .service import (
    create_journal_entry,
    get_recent_entries,
    get_entry_by_id,
    update_journal_entry,
    delete_journal_entry,
    toggle_favorite,
    get_favorites,
    get_past_reflections,
    get_calendar_data,
    get_user_current_streak,
    get_daily_prompt,
    get_user_stats
)

logger = logging.getLogger("zenark.journaling.routes")

router = APIRouter(prefix="/journal", tags=["Journaling"])


@router.post("/entry")
async def create_entry(request: Request):
    """
    Create a new journal entry
    
    Request Body:
    {
        "user_id": "user123",
        "mood": "😊",
        "title": "Finding stillness in chaos",
        "content": "Today was overwhelming...",
        "tags": ["#calm", "#work"],
        "time_spent": 320
    }
    """
    try:
        data = await request.json()
        
        # Validate required fields
        user_id = data.get("user_id")
        mood = data.get("mood")
        title = data.get("title")
        content = data.get("content")
        tags = data.get("tags", [])
        time_spent = data.get("time_spent", 0)
        
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        if not title or len(title) < 3:
            raise HTTPException(status_code=400, detail="Title must be at least 3 characters")
        if not content or len(content) < 10:
            raise HTTPException(status_code=400, detail="Content must be at least 10 characters")
        if mood not in ["😊", "😃", "😐", "😢"]:
            raise HTTPException(status_code=400, detail="Invalid mood emoji")
        
        # Create entry
        result = await create_journal_entry(
            user_id=user_id,
            mood=mood,
            title=title,
            content=content,
            tags=tags,
            time_spent=time_spent
        )
        
        return JSONResponse({
            "success": True,
            "entry_id": result["entry_id"],
            "message": "Journal entry saved successfully",
            "streak_updated": result["streak_updated"],
            "current_streak": result["current_streak"]
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating journal entry: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent-entries")
async def get_recent(user_id: str, limit: int = 5):
    """
    Get user's recent journal entries
    
    Query Params:
    - user_id: User identifier
    - limit: Number of entries to return (default: 5)
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        entries = await get_recent_entries(user_id, limit)
        
        return JSONResponse({
            "success": True,
            "recent_entries": entries,
            "total": len(entries)
        })
        
    except Exception as e:
        logger.error(f"Error getting recent entries: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/entry/{entry_id}")
async def get_entry(entry_id: str, user_id: str):
    """
    Get a specific journal entry by ID
    
    Path Params:
    - entry_id: Entry identifier
    
    Query Params:
    - user_id: User identifier
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        entry = await get_entry_by_id(entry_id, user_id)
        
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        return JSONResponse({
            "success": True,
            "entry": entry
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting entry: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/entry/{entry_id}")
async def update_entry(entry_id: str, request: Request):
    """
    Update an existing journal entry
    
    Path Params:
    - entry_id: Entry identifier
    
    Request Body:
    {
        "user_id": "user123",
        "mood": "😊",  // optional
        "title": "Updated title",  // optional
        "content": "Updated content",  // optional
        "tags": ["#new", "#tags"]  // optional
    }
    """
    try:
        data = await request.json()
        user_id = data.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        success = await update_journal_entry(
            entry_id=entry_id,
            user_id=user_id,
            mood=data.get("mood"),
            title=data.get("title"),
            content=data.get("content"),
            tags=data.get("tags")
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Entry not found or not updated")
        
        return JSONResponse({
            "success": True,
            "message": "Entry updated successfully"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating entry: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/entry/{entry_id}")
async def delete_entry(entry_id: str, user_id: str):
    """
    Delete a journal entry
    
    Path Params:
    - entry_id: Entry identifier
    
    Query Params:
    - user_id: User identifier
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        success = await delete_journal_entry(entry_id, user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        return JSONResponse({
            "success": True,
            "message": "Entry deleted successfully"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting entry: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/favorite/{entry_id}")
async def toggle_entry_favorite(entry_id: str, user_id: str):
    """
    Toggle favorite status of an entry
    
    Path Params:
    - entry_id: Entry identifier
    
    Query Params:
    - user_id: User identifier
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        result = await toggle_favorite(entry_id, user_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("error", "Entry not found"))
        
        return JSONResponse(result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error toggling favorite: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/favorites")
async def get_user_favorites(user_id: str):
    """
    Get all favorite entries for a user
    
    Query Params:
    - user_id: User identifier
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        favorites = await get_favorites(user_id)
        
        return JSONResponse({
            "success": True,
            "favorites": favorites,
            "total": len(favorites)
        })
        
    except Exception as e:
        logger.error(f"Error getting favorites: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/past-reflections")
async def get_reflections(user_id: str, date: Optional[str] = None):
    """
    Get journal entries for a specific date
    
    Query Params:
    - user_id: User identifier
    - date: Date in YYYY-MM-DD format (optional, defaults to today)
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        target_date = None
        if date:
            try:
                target_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        result = await get_past_reflections(user_id, target_date)
        
        return JSONResponse({
            "success": True,
            **result
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting past reflections: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calendar-data")
async def get_calendar(user_id: str, year: int, month: int):
    """
    Get calendar data showing which dates have entries
    
    Query Params:
    - user_id: User identifier
    - year: Year (e.g., 2025)
    - month: Month (1-12)
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        if not (1 <= month <= 12):
            raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
        if year < 2000 or year > 2100:
            raise HTTPException(status_code=400, detail="Invalid year")
        
        result = await get_calendar_data(user_id, year, month)
        
        return JSONResponse({
            "success": True,
            **result
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting calendar data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/streak")
async def get_streak(user_id: str):
    """
    Get user's current journaling streak
    
    Query Params:
    - user_id: User identifier
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        current_streak = await get_user_current_streak(user_id)
        
        return JSONResponse({
            "success": True,
            "current_streak": current_streak
        })
        
    except Exception as e:
        logger.error(f"Error getting streak: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/daily-prompt")
async def get_prompt():
    """
    Get today's daily journaling prompt
    """
    try:
        prompt = await get_daily_prompt()
        
        return JSONResponse({
            "success": True,
            "prompt": prompt
        })
        
    except Exception as e:
        logger.error(f"Error getting daily prompt: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats(user_id: str):
    """
    Get comprehensive statistics for a user
    
    Query Params:
    - user_id: User identifier
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        stats = await get_user_stats(user_id)
        
        return JSONResponse({
            "success": True,
            "stats": stats.dict()
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
