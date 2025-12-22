"""
Database setup and operations for Journaling feature
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from typing import Optional
import os
import logging

logger = logging.getLogger("zenark.journaling")

# Global collections
journal_entries_col: Optional[AsyncIOMotorCollection] = None
journal_streaks_col: Optional[AsyncIOMotorCollection] = None
daily_prompts_col: Optional[AsyncIOMotorCollection] = None


async def init_journaling_db(client: AsyncIOMotorClient, db_name: str):
    """
    Initialize journaling database collections
    
    Args:
        client: MongoDB client instance
        db_name: Database name
    """
    global journal_entries_col, journal_streaks_col, daily_prompts_col
    
    try:
        db = client[db_name]
        
        # Initialize collections
        journal_entries_col = db["journal_entries"]
        journal_streaks_col = db["journal_streaks"]
        daily_prompts_col = db["daily_prompts"]
        
        # Create indexes for better performance
        await journal_entries_col.create_index("user_id")
        await journal_entries_col.create_index("timestamp")
        await journal_entries_col.create_index([("user_id", 1), ("timestamp", -1)])
        await journal_entries_col.create_index([("user_id", 1), ("is_favorite", 1)])
        await journal_entries_col.create_index("tags")
        
        await journal_streaks_col.create_index("user_id", unique=True)
        
        await daily_prompts_col.create_index("prompt_id", unique=True)
        await daily_prompts_col.create_index("active")
        
        logger.info("✅ Journaling database initialized successfully")
        
        # Seed daily prompts if collection is empty
        await seed_daily_prompts()
        
    except Exception as e:
        logger.error(f"❌ Error initializing journaling database: {e}")
        raise


async def seed_daily_prompts():
    """Seed the database with initial daily prompts"""
    
    if await daily_prompts_col.count_documents({}) > 0:
        return  # Already seeded
    
    prompts = [
        {
            "prompt_id": "prompt_001",
            "text": "What is one small thing you can control today?",
            "category": "reflection",
            "active": True
        },
        {
            "prompt_id": "prompt_002",
            "text": "What are three things you're grateful for right now?",
            "category": "gratitude",
            "active": True
        },
        {
            "prompt_id": "prompt_003",
            "text": "What emotion are you feeling most strongly today, and why?",
            "category": "emotions",
            "active": True
        },
        {
            "prompt_id": "prompt_004",
            "text": "What is one goal you want to accomplish this week?",
            "category": "goals",
            "active": True
        },
        {
            "prompt_id": "prompt_005",
            "text": "Describe a moment today that made you smile.",
            "category": "reflection",
            "active": True
        },
        {
            "prompt_id": "prompt_006",
            "text": "What challenge are you facing, and what's one step you can take?",
            "category": "reflection",
            "active": True
        },
        {
            "prompt_id": "prompt_007",
            "text": "Who in your life are you thankful for, and why?",
            "category": "gratitude",
            "active": True
        },
        {
            "prompt_id": "prompt_008",
            "text": "What does success look like for you today?",
            "category": "goals",
            "active": True
        },
        {
            "prompt_id": "prompt_009",
            "text": "How are you taking care of yourself today?",
            "category": "reflection",
            "active": True
        },
        {
            "prompt_id": "prompt_010",
            "text": "What lesson did you learn recently?",
            "category": "reflection",
            "active": True
        }
    ]
    
    await daily_prompts_col.insert_many(prompts)
    logger.info(f"✅ Seeded {len(prompts)} daily prompts")


def get_journal_entries_collection() -> AsyncIOMotorCollection:
    """Get journal entries collection"""
    if journal_entries_col is None:
        raise RuntimeError("Journaling database not initialized")
    return journal_entries_col


def get_journal_streaks_collection() -> AsyncIOMotorCollection:
    """Get journal streaks collection"""
    if journal_streaks_col is None:
        raise RuntimeError("Journaling database not initialized")
    return journal_streaks_col


def get_daily_prompts_collection() -> AsyncIOMotorCollection:
    """Get daily prompts collection"""
    if daily_prompts_col is None:
        raise RuntimeError("Journaling database not initialized")
    return daily_prompts_col
