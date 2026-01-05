"""
Database setup for Meditation feature
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from typing import Optional
import os

logger = logging.getLogger("zenark.meditation.database")

# Global database connection
_meditation_progress_col: Optional[AsyncIOMotorCollection] = None
_meditation_streaks_col: Optional[AsyncIOMotorCollection] = None


async def init_meditation_db(mongo_client: AsyncIOMotorClient):
    """
    Initialize meditation database collections
    
    Args:
        mongo_client: MongoDB client instance
    """
    global _meditation_progress_col, _meditation_streaks_col
    
    try:
        db_name = os.getenv("MONGO_DB_OFFICIAL", "zenark_official")
        db = mongo_client[db_name]
        
        # Meditation progress collection
        _meditation_progress_col = db["meditation_progress"]
        await _meditation_progress_col.create_index([("user_id", 1), ("session_id", 1)], unique=True)
        await _meditation_progress_col.create_index([("user_id", 1)])
        
        # Meditation streaks collection
        _meditation_streaks_col = db["meditation_streaks"]
        await _meditation_streaks_col.create_index([("user_id", 1)], unique=True)
        
        logger.info("✅ Meditation database initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize meditation database: {e}")
        raise


def get_meditation_progress_collection() -> AsyncIOMotorCollection:
    """Get meditation progress collection"""
    if _meditation_progress_col is None:
        raise RuntimeError("Meditation database not initialized")
    return _meditation_progress_col


def get_meditation_streaks_collection() -> AsyncIOMotorCollection:
    """Get meditation streaks collection"""
    if _meditation_streaks_col is None:
        raise RuntimeError("Meditation database not initialized")
    return _meditation_streaks_col
