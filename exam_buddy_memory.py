"""
MongoDB-based Chat Memory for Exam Buddy
Maintains conversation history using user_id instead of session_id
"""

from motor.motor_asyncio import AsyncIOMotorCollection
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger("zenark.exam_buddy_memory")


class ExamBuddyMongoMemory:
    """
    MongoDB-based memory for Exam Buddy that uses user_id for persistence.
    This ensures conversation history is maintained across sessions.
    """
    
    def __init__(self, user_id: str, collection: AsyncIOMotorCollection):
        """
        Initialize MongoDB memory for exam buddy.
        
        Args:
            user_id: User identifier (from JWT token)
            collection: MongoDB collection for storing conversations
        """
        self.user_id = user_id
        self.collection = collection
        self.history = ChatMessageHistory()
        self.loaded = False
    
    async def load_history(self):
        """Load existing conversation history from MongoDB"""
        if self.loaded:
            return
        
        try:
            # Find the user's exam buddy conversation
            doc = await self.collection.find_one({
                "user_id": self.user_id,
                "chat_type": "exam_buddy"
            })
            
            if doc and "messages" in doc:
                # Reconstruct chat history
                for msg in doc["messages"]:
                    if msg.get("role") == "user":
                        self.history.add_user_message(msg.get("content", ""))
                    elif msg.get("role") == "assistant":
                        self.history.add_ai_message(msg.get("content", ""))
                
                logger.info(f"✅ Loaded {len(doc['messages'])} messages for user {self.user_id}")
            else:
                logger.info(f"📝 No existing exam buddy history for user {self.user_id}")
            
            self.loaded = True
            
        except Exception as e:
            logger.error(f"Error loading exam buddy history: {e}")
            self.loaded = True  # Mark as loaded to prevent retry loops
    
    async def add_user_message(self, message: str):
        """Add user message to history and save to MongoDB"""
        self.history.add_user_message(message)
        await self._save_to_db()
    
    async def add_ai_message(self, message: str):
        """Add AI message to history and save to MongoDB"""
        self.history.add_ai_message(message)
        await self._save_to_db()
    
    async def _save_to_db(self):
        """Save current conversation to MongoDB"""
        try:
            # Convert chat history to serializable format
            messages = []
            for msg in self.history.messages:
                if isinstance(msg, HumanMessage):
                    messages.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    messages.append({"role": "assistant", "content": msg.content})
            
            # Upsert to MongoDB
            await self.collection.update_one(
                {
                    "user_id": self.user_id,
                    "chat_type": "exam_buddy"
                },
                {
                    "$set": {
                        "messages": messages,
                        "updated_at": datetime.datetime.utcnow()
                    },
                    "$setOnInsert": {
                        "created_at": datetime.datetime.utcnow()
                    }
                },
                upsert=True
            )
            
        except Exception as e:
            logger.error(f"Error saving exam buddy history: {e}")
    
    def get_messages(self) -> List:
        """Get all messages in the conversation"""
        return self.history.messages
    
    async def clear_history(self):
        """Clear conversation history"""
        self.history.clear()
        await self.collection.delete_one({
            "user_id": self.user_id,
            "chat_type": "exam_buddy"
        })
        logger.info(f"🗑️ Cleared exam buddy history for user {self.user_id}")


# Global storage for memory instances (keyed by user_id)
_memory_store: Dict[str, ExamBuddyMongoMemory] = {}


async def get_exam_buddy_memory(user_id: str, collection: AsyncIOMotorCollection) -> ExamBuddyMongoMemory:
    """
    Get or create exam buddy memory for a user.
    
    Args:
        user_id: User identifier
        collection: MongoDB collection
    
    Returns:
        ExamBuddyMongoMemory instance
    """
    if user_id not in _memory_store:
        memory = ExamBuddyMongoMemory(user_id, collection)
        await memory.load_history()
        _memory_store[user_id] = memory
    
    return _memory_store[user_id]
