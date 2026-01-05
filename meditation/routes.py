"""
FastAPI Routes for Meditation Feature
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional
import logging
import os

from .data import get_all_sessions, get_session_by_id, get_sessions_by_tab
from .service import (
    mark_session_complete,
    get_user_progress,
    get_current_streak,
    get_meditation_stats
)

logger = logging.getLogger("zenark.meditation.routes")

router = APIRouter(prefix="/meditation", tags=["Meditation"])


@router.get("/sessions")
async def get_sessions(tab: Optional[int] = None):
    """
    Get all meditation sessions or filter by tab
    
    Query Params:
    - tab: Optional tab number (1 or 2)
    """
    try:
        if tab:
            if tab not in [1, 2]:
                raise HTTPException(status_code=400, detail="Tab must be 1 or 2")
            sessions = get_sessions_by_tab(tab)
        else:
            sessions = get_all_sessions()
        
        return JSONResponse({
            "success": True,
            "sessions": sessions,
            "total": len(sessions)
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """
    Get a specific meditation session by ID
    
    Path Params:
    - session_id: Session ID (101-104, 201-210)
    """
    try:
        session = get_session_by_id(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return JSONResponse({
            "success": True,
            "session": session
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/audio/{session_id}")
async def get_audio(session_id: str):
    """
    Get meditation audio file
    
    Path Params:
    - session_id: Session ID (101-104, 201-210)
    """
    try:
        session = get_session_by_id(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get audio file path
        audio_file = session["audio_file"]
        audio_path = os.path.join("meditation audios", audio_file)
        
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename=audio_file
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/complete")
async def complete_session(request: Request):
    """
    Mark a meditation session as complete
    
    Request Body:
    {
        "user_id": "user123",
        "session_id": "201",
        "time_spent": 600
    }
    """
    try:
        data = await request.json()
        
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        time_spent = data.get("time_spent", 0)
        
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        if not session_id:
            raise HTTPException(status_code=400, detail="session_id is required")
        
        result = await mark_session_complete(user_id, session_id, time_spent)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to complete session"))
        
        return JSONResponse(result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error completing session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/progress")
async def get_progress(user_id: str):
    """
    Get user's meditation progress
    
    Query Params:
    - user_id: User identifier
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        progress = await get_user_progress(user_id)
        
        return JSONResponse({
            "success": True,
            "progress": progress,
            "total_completed": len(progress)
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting progress: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/streak")
async def get_streak(user_id: str):
    """
    Get user's current meditation streak
    
    Query Params:
    - user_id: User identifier
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        current_streak = await get_current_streak(user_id)
        
        return JSONResponse({
            "success": True,
            "current_streak": current_streak
        })
        
    except Exception as e:
        logger.error(f"Error getting streak: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats(user_id: str):
    """
    Get comprehensive meditation statistics
    
    Query Params:
    - user_id: User identifier
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        stats = await get_meditation_stats(user_id)
        
        return JSONResponse({
            "success": True,
            "stats": stats.dict()
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
